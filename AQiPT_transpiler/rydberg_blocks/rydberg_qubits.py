from typing import Any, List, Dict, Optional, Union
import matplotlib.pyplot as plt
from itertools import product
import qutip as qt
from AQiPT import AQiPTcore as aqipt
from AQiPT.modules.emulator import AQiPTemulator as emulator


from ..config.core import BackendConfig, default_backend
from ..rydberg_blocks.rydberg_schedules import (
    RydbergQubitSchedule,
    RydbergRegisterSchedule,
)


class RydbergQubit:
    def __init__(
        self,
        nr_levels: int = 4,
        rydberg_states: Dict[str, Any] = default_backend.atomic_config.rydberg_states,
        dissipators: Dict[str, Any] = {"Dissipator0": [[0, 0], 0]},
        initial_state: Optional[Union[int, qt.Qobj]] = 0,
        name: Optional[str] = "qubit",
        schedule: Optional[RydbergQubitSchedule] = None,
        **kwargs,
    ):
        self.nr_levels = nr_levels
        self.rydberg_states = rydberg_states
        self.dissipators = dissipators
        self.initial_state = initial_state
        self.name = name
        self.schedule = schedule
        self.atom = None

        if "backend" in kwargs.keys():
            backend_config = kwargs["backend"]
            assert isinstance(backend_config, BackendConfig)

            self.backend_config = backend_config

        else:
            self.backend_config = default_backend

    def compile(self):
        nr_levels = self.nr_levels
        psi0 = self.initial_state

        couplings_q = self.schedule.coupling_pulses
        detunings_q = self.schedule.detuning_pulses
        dissipators_q = self.dissipators
        rydbergstates_q = self.rydberg_states

        sim_params_q = {
            "couplings": couplings_q,
            "detunings": detunings_q,
            "dissipators": dissipators_q,
            "rydbergstates": rydbergstates_q,
        }

        simulation_config = self.backend_config.simulation_config
        pulsed_qubit = emulator.atomicModel(
            self.schedule.times,
            nr_levels,
            psi0,
            sim_params_q,
            name=self.name,
            simOpt=qt.Options(
                nsteps=simulation_config.nsteps,
                rtol=simulation_config.rtol,
                max_step=simulation_config.max_steps,
                store_states=simulation_config.store_states,
            ),
        )
        pulsed_qubit.modelMap(plotON=False)

        pulsed_qubit.buildTHamiltonian()
        pulsed_qubit.buildHamiltonian()

        for diss in self.dissipators.values():
            if diss[1] != 0:
                pulsed_qubit.buildLindbladians()
                break

        pulsed_qubit.buildObservables()
        self.atom = pulsed_qubit

    def sim(self):
        self.atom.playSim(mode="control")

    def build(self):
        self.compile()
        self.sim()

    def __str__(self):
        return f"{self.name}"

    def plot_results(self):
        pulse_config = self.backend_config.pulse_config
        other_color = pulse_config.DEFAULT_COLORS["other"]

        simRes = self.atom.getResult()

        states = simRes.expect
        sl = len(states)

        fig, axis = plt.subplots(sl, figsize=(16, 2 * sl))

        plt.setp(axis, yticks=[0, 0.5, 1])
        times = self.schedule.times
        for i in range(sl):
            state = states[i]

            axis[i].plot(times, state, color=other_color[i % 4])
            axis[i].set_ylabel(f"State {i}", fontsize=14)
            axis[i].set_ylim(0, 1)
            axis[i].vlines(
                x=range(0, 12, 2), ymin=0, ymax=1, color="silver", linestyle="dotted"
            )
            axis[i].spines["top"].set_visible(False)
            axis[i].spines["right"].set_visible(False)
            if i != sl - 1:
                axis[i].get_xaxis().set_visible(False)

            plt.yticks([0, 0.5, 1])

        fig.suptitle("Population evolution", fontsize=24)
        fig.supxlabel("Time", fontsize=18)
        plt.show()


class RydbergQuantumRegister:
    def __init__(
        self,
        qubits: List[RydbergQubit],
        layout: List[tuple] = default_backend.atomic_config.layout,
        init_state: Union[str, qt.Qobj, Any] = None,
        name: str = "Quantum Register",
        connectivity: Optional[List[Any]] = default_backend.atomic_config.connectivity,
        c6: float = default_backend.atomic_config.c6_constant,
        c3: float = default_backend.atomic_config.c3_constant,
        **kwargs,
    ):
        self.qubits = qubits
        self.layout = layout
        if isinstance(init_state, str):
            self.init_state = (
                str(0).zfill(len(qubits)) if init_state == None else init_state
            )
        else:
            self.init_state = init_state
        self.name = name
        self.connectivity = connectivity
        self.c6 = c6
        self.c3 = c3

        if "backend" in kwargs.keys():
            backend_config = kwargs["backend"]
            assert isinstance(backend_config, BackendConfig)
            self.backend_config = backend_config
        else:
            self.backend_config = default_backend

        simulation_config = self.backend_config.simulation_config
        sampling = simulation_config.sampling
        bitdepth = simulation_config.bitdepth
        t_max = simulation_config.time_simulation

        self.times = aqipt.general_params(
            {"sampling": sampling, "bitdepth": bitdepth, "time_dyn": t_max}
        ).timebase()

        self.atomic_register = None
        self.schedule = {}

    def _atoms(self):
        atoms = []
        for qubit in self.qubits:
            if qubit.atom is not None:
                qubit.build()
            atom = qubit.atom

            atoms.append(atom)

        return atoms

    def compile(self):
        atomic_register = emulator.atomicQRegister(
            physicalRegisters=self._atoms(),
            initnState=self.init_state,
            name=self.name,
            connectivity=self.connectivity,
            layout=self.layout,
        )

        self._schedule()
        atomic_register.buildNinitState()

        atomic_register.buildTNHamiltonian()

        atomic_register.registerMap(plotON=False, figure_size=(3, 3))

        simulation_config = self.backend_config.simulation_config
        atomic_register.simOpts = qt.Options(
            nsteps=simulation_config.nsteps,
            rtol=simulation_config.rtol,
            max_step=simulation_config.max_steps,
            store_states=simulation_config.store_states,
        )
        atomic_register.compile()
        atomic_register.buildInteractions(c6=self.c6, c3=self.c3)

        # atomic_register.buildNLindbladians()

        atomic_register.buildNObservables()

        self.atomic_register = atomic_register

    def sim(self):
        self.atomic_register.playSim(mode="control")

    def build(self):
        self.compile()
        self.sim()

    def _schedule(self):
        qubits_sch = [qubit.schedule for qubit in self.qubits]

        ryd_sche = RydbergRegisterSchedule(qubits_sch, backend=self.backend_config)
        self.schedule = ryd_sche

    def plot_schedule(self, couplings=True, detunings=False):
        pulse_config = self.backend_config.pulse_config
        coupling_color = pulse_config.DEFAULT_COLORS["coupling"]
        detuning_color = pulse_config.DEFAULT_COLORS["detuning"]

        self.schedule.plot_schedule(
            couplings, detunings, coupling_color, detuning_color
        )

    def plot_results(self):
        pulse_config = self.backend_config.pulse_config
        other_color = pulse_config.DEFAULT_COLORS["other"]

        simRes = self.atomic_register.getResult()

        states = simRes.expect
        sl = len(states)

        levels = self.qubits[0].rydberg_states["l_values"]
        perm_lev = list(product(levels, repeat=len(self.qubits)))

        fig, axis = plt.subplots(sl, figsize=(16, 1.7 * sl))

        plt.setp(axis, yticks=[0, 0.5, 1])
        times = self.times
        for i in range(sl):
            state = states[i]

            axis[i].plot(times, state, color=other_color[i % 4])
            axis[i].set_ylabel(f"State {perm_lev[i]}", fontsize=14)
            axis[i].set_ylim(0, 1)
            axis[i].vlines(
                x=range(0, 12, 2), ymin=0, ymax=1, color="silver", linestyle="dotted"
            )
            axis[i].spines["top"].set_visible(False)
            axis[i].spines["right"].set_visible(False)
            if i != sl - 1:
                axis[i].get_xaxis().set_visible(False)

            plt.yticks([0, 0.5, 1])

        fig.suptitle("Population evolution", fontsize=24)
        fig.supxlabel("Time", fontsize=18)
        plt.show()
