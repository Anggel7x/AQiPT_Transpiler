import qutip as qt
import matplotlib.pyplot as plt
from AQiPT.modules.emulator import AQiPTemulator as emulator
from .shaped_pulses import *
from typing import Any, List, Dict, Optional
from itertools import product

from transpiler.config.core import backend
from transpiler.rydberg_blocks.rydberg_schedules import RydbergQubitSchedule, RydbergRegisterSchedule


simulation_config = backend.simulation_config
T_MAX = simulation_config.time_simulation

pulse_config = backend.pulse_config
PULSE_PARAMS = backend.simulation_config.PULSE_PARAMS

coupling_color = pulse_config.DEFAULT_COLORS['coupling']
detuning_color = pulse_config.DEFAULT_COLORS['detuning']
other_color = pulse_config.DEFAULT_COLORS['other']
style = pulse_config.ploting_style


class RydbergQubit():

    def __init__(self,
        nr_levels: int = 2,
        rydberg_states: Dict[str, Any] = {'RydbergStates': [], 'l_values':[]}, 
        dissipators: Dict[str, Any] = {'Dissipator0': [[0,0], 0]},
        initial_state: Optional[int] = 0,
        name: Optional[str] = 'qubit',
        schedule: Optional[RydbergQubitSchedule] = None,
    ):
        self.nr_levels = nr_levels
        self.rydberg_states = rydberg_states
        self.dissipators = dissipators
        self.initial_state = initial_state
        self.name = name
        self.schedule = schedule
        self.atom = None

    def build(self):

        Nrlevels = self.nr_levels
        psi0 = self.initial_state

        times = self.schedule.times

        couplings_q = self.schedule.coupling_pulses
        detunings_q = self.schedule.detuning_pulses
        dissipators_q = self.dissipators
        rydbergstates_q = self.rydberg_states

        sim_params_q = {
                'couplings': couplings_q, 
                'detunings': detunings_q, 
                'dissipators': dissipators_q,
                'rydbergstates': rydbergstates_q}; 

        pulsed_qubit = emulator.atomicModel(times, Nrlevels, psi0, sim_params_q, name=self.name, simOpt=qt.Options(nsteps=120000, rtol=1e-6, max_step=10e-6, store_states=True))
        pulsed_qubit.modelMap(plotON=False)

        pulsed_qubit.buildTHamiltonian()
        pulsed_qubit.buildHamiltonian()
        try:
            pulsed_qubit.buildLindbladians()
        except:
            pass
        pulsed_qubit.buildObservables()

        pulsed_qubit.playSim(mode='control')

        self.atom = pulsed_qubit

    def __str__(self):
        print('{self.name}')
    
    def plot_results(self , color = other_color):
        simRes = self.atom.getResult()
        
        states = simRes.expect
        sl = len(states)

        fig, axis = plt.subplots(sl, figsize=(16, 2*sl))

        plt.setp(axis, yticks=[0, 0.5, 1])
        times = self.schedule.times
        for i in range(sl):
            state = states[i]
            
            axis[i].plot(times, state, color=color[i % 4])
            axis[i].set_ylabel(f'State {i}', fontsize=14)
            axis[i].set_ylim(0,1)
            axis[i].vlines(x = range(0,12,2), ymin = 0, ymax =1, color = 'silver', linestyle='dotted')
            axis[i].spines['top'].set_visible(False)
            axis[i].spines['right'].set_visible(False)
            if i != sl-1:
                axis[i].get_xaxis().set_visible(False)
                
                
            plt.yticks([0,0.5,1])

        fig.suptitle('Population evolution', fontsize=24)
        fig.supxlabel('Time', fontsize=18)
        plt.show()

class RydbergQuantumRegister():

    def __init__(self,
        qubits: List[RydbergQubit],
        layout,
        init_state: str = None,
        name: str = 'Quantum Register',
        connectivity: Optional[List[Any]] = ['All', []],
        c6: float = 0,
        c3: float = 0,
        times = PULSE_PARAMS.timebase()
    ):

        self.qubits = qubits
        self.layout = layout
        if isinstance(init_state, str):
            self.init_state = str(0).zfill(len(qubits)) if init_state == None else init_state
        else:
            self.init_state = init_state
        self.name = name
        self.connectivity = connectivity
        self.c6 = c6
        self.c3 = c3
        self.times = times

        self.atomic_register = None
        self.schedule = {}
        
    def _atoms(self):

        atoms = []
        for qubit in self.qubits:
            
            if qubit.atom == None:
                qubit.build()
            atom = qubit.atom

            atoms.append(atom)        
        
        return atoms

    def _build(self, nsteps=10000, rtol=1e-6, max_steps=10e-6):

        atomic_register = emulator.atomicQRegister(
            physicalRegisters= self._atoms(),
            initnState = self.init_state,
            name = self.name,
            connectivity= self.connectivity,
            layout = self.layout
        )

        self._schedule()
        atomic_register.buildTNHamiltonian(); 
        atomic_register.registerMap(plotON=False, figure_size=(3,3)); 

        atomic_register.simOpts = qt.Options(nsteps=nsteps, rtol=rtol, max_step=max_steps, store_states=True)
        return atomic_register

    def compile(self, nsteps=10e3, rtol=1e-6, max_steps = 10e-6):
        atomic_register = self._build(nsteps=nsteps, rtol=rtol, max_steps=max_steps)
        atomic_register.compile()
        atomic_register.buildInteractions(c6=self.c6, c3=self.c3); 
        
        try:
            atomic_register.buildNLindbladians()
        except:
            pass
        atomic_register.buildNObservables()
        atomic_register.buildNinitState()

        atomic_register.playSim(mode='control')

        self.atomic_register = atomic_register

    def _schedule(self):
        qubits_sch = [qubit.schedule for qubit in self.qubits]
            
            
        ryd_sche = RydbergRegisterSchedule(qubits_sch)
        self.schedule = ryd_sche

    def plot_schedule(self, xmin=0, xmax=T_MAX, couplings=True, detunings=False, color_coup =coupling_color, color_det=detuning_color):

        self.schedule.plot_schedule(xmin, xmax, couplings, detunings, color_coup, color_det)

    def plot_results(self , color = other_color):
        simRes = self.atomic_register.getResult()
        
        states = simRes.expect
        sl = len(states)

        levels = self.qubits[0].rydberg_states['l_values']
        perm_lev = list(product(levels, repeat=len(self.qubits)))


        fig, axis = plt.subplots(sl, figsize=(16, 1.7*sl))

        plt.setp(axis, yticks=[0, 0.5, 1])
        times = self.times
        for i in range(sl):
            state = states[i]
            
            axis[i].plot(times, state, color=color[i%4])
            axis[i].set_ylabel(f'State {perm_lev[i]}', fontsize=14)
            axis[i].set_ylim(0,1)
            axis[i].vlines(x = range(0,12,2), ymin = 0, ymax =1, color = 'silver', linestyle='dotted')
            axis[i].spines['top'].set_visible(False)
            axis[i].spines['right'].set_visible(False)
            if i != sl-1:
                axis[i].get_xaxis().set_visible(False)
                
                
            plt.yticks([0,0.5,1])

        fig.suptitle('Population evolution', fontsize=24)
        fig.supxlabel('Time', fontsize=18)
        plt.show()
