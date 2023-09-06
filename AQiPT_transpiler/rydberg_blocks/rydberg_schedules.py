from typing import Any, List
import numpy as np
import matplotlib.pyplot as plt
from AQiPT import AQiPTcore as aqipt
from ..utils.schedules_utils import merge_pulses
from ..config.core import BackendConfig, default_backend

plt.style.use("dark_background")


class RydbergQubitSchedule:
    r"""Clase que contiene los parámetros del schedule dedicado para un solo átomos."""

    def __init__(self, coupling_pulses: Any, detuning_pulses: Any, **kwargs):
        self.coupling_pulses = coupling_pulses
        self.detuning_pulses = detuning_pulses

        self._merge_pulses()
        self.q_schedule = self

        if "backend" in kwargs:
            backend_config = kwargs["backend"]
            assert isinstance(backend_config, BackendConfig)

            self.backend_config = backend_config

        else:
            self.backend_config = None

        simulation_config = self.backend_config.simulation_config
        sampling = simulation_config.sampling
        bitdepth = simulation_config.bitdepth
        t_max = simulation_config.time_simulation

        self.times = aqipt.general_params(
            {"sampling": sampling, "bitdepth": bitdepth, "time_dyn": t_max}
        ).timebase()

    def _merge_pulses(self):
        self.coupling_pulses = merge_pulses(self.coupling_pulses, "Coupling")
        self.detuning_pulses = merge_pulses(self.detuning_pulses, "Detuning")

    def add_function(self, funct: np.ndarray, where: str, funct_type="coupling"):
        r"""Añase una función a un schedule.

        Args:
            funct (np.ndarray): Función a añadir.
            where (str): Ubicación dentro del schedule
            funct_type (str, optional): Tipo de función. Defaults to "coupling".

        Raises:
            ValueError: No se especifico el tipo de función.
        """
        if funct_type == "coupling":
            schedule1 = self.coupling_pulses
        elif funct_type == "detuning":
            schedule1 = self.detuning_pulses
        else:
            raise ValueError
        funct_1 = schedule1[where][2]

        funct_1 += funct

        schedule1[where][2] = funct_1

    def add_coupling(self, schedule2: dict, what: str, funct_type="coupling"):
        r"""Añade un schedule al schedule del qubit.
        Args:
            schedule2 (dict): Schedule que se desea agregar.
            what (str): Qué se desea agregar del schedule2.
            funct_type (str, optional): Tipo de función a agregar.. Defaults to "coupling".

        Raises:
            ValueError: No se definió bien el tipo de función.
        """
        if funct_type == "coupling":
            schedule1 = self.coupling_pulses
        elif funct_type == "detuning":
            schedule1 = self.detuning_pulses
        else:
            raise ValueError

        val = schedule2[what]
        schedule1[what] = val

    def plot_couplings(
        self, plot: bool = True, name: str = "", phase=True, amp=True
    ) -> Any:
        """Función que hace el plot de las funciones de acople con sus pares.

        Args:
            plot (bool, optional): Si se desea devolver la figura o no. Defaults to True.
            name (str, optional): Nombre del plot. Defaults to "".
            phase (bool, optional): Si se desea indicar las fases de los pulsos. Defaults to True.
            amp (bool, optional): Si se desea indicar las amplitudes de los pulsos. Defaults to True.

        Returns:
            Any: Figura del plot.
        """
        times = self.times
        p_pulses = {}

        pulse_config = self.backend_config.pulse_config
        coupling_color = pulse_config.DEFAULT_COLORS["coupling"]

        for key in self.coupling_pulses.keys():
            pair = self.coupling_pulses[key][0]
            omega = self.coupling_pulses[key][1]
            p_pulses[str(pair) + str(omega)] = []

        for key in self.coupling_pulses.keys():
            pair = self.coupling_pulses[key][0]
            pulse = self.coupling_pulses[key][-1]
            omega = self.coupling_pulses[key][1]
            p_pulses[str(pair) + str(omega)].append((pulse, omega))

        L = len(p_pulses.keys())
        fig, axis = plt.subplots(L, figsize=(16, 2 * L))

        for i in range(L):
            key = list(p_pulses.keys())[i]

            if L == 1:
                for pulse, omega in p_pulses[key]:
                    factor = omega / (2 * np.pi)
                    max_amp = np.max(np.abs(pulse))

                    abs_pulse = np.abs(pulse) / max_amp
                    angl_pulse = -np.angle(pulse)

                    if phase:
                        axis.plot(
                            times,
                            angl_pulse,
                            color=coupling_color[i + 1 % 4],
                            label="$\phi (t)$",
                        )
                        axis.fill_between(
                            times,
                            angl_pulse,
                            color=coupling_color[i + 1 % 4],
                            alpha=0.2,
                        )
                    if amp:
                        axis.plot(
                            times,
                            abs_pulse,
                            color=coupling_color[i % 4],
                            label="$\Omega (t)$",
                        )
                        axis.fill_between(
                            times, abs_pulse, color=coupling_color[i % 4], alpha=0.3
                        )

                    if factor != 1:
                        axis.text(
                            0.01,
                            0.99,
                            f"$\Omega = 2\pi{factor:0.2f}$",
                            ha="left",
                            va="top",
                            transform=axis.transAxes,
                        )

                axis.set_ylabel(f"{key[:6]}")

                axis.legend()
            else:
                for pulse, omega in p_pulses[key]:
                    factor = omega / (2 * np.pi)
                    max_amp = np.max(np.abs(pulse))

                    abs_pulse = np.abs(pulse)
                    angl_pulse = -np.angle(pulse)

                    if phase:
                        axis[i].plot(
                            times,
                            angl_pulse,
                            color=coupling_color[1],
                            label="$\phi (t)$",
                        )
                        axis[i].fill_between(
                            times, angl_pulse, color=coupling_color[1], alpha=0.2
                        )
                    if amp:
                        axis[i].plot(
                            times,
                            abs_pulse,
                            color=coupling_color[0],
                            label="$\Omega (t)$",
                        )
                        axis[i].fill_between(
                            times, abs_pulse, color=coupling_color[0], alpha=0.3
                        )

                    axis[i].text(
                        0.01,
                        0.99,
                        f"$\Omega = 2\pi{factor:0.2f}$",
                        ha="left",
                        va="top",
                        transform=axis[i].transAxes,
                    )

                axis[i].set_ylabel(f"{key[:6]}")
                axis[i].legend()

        fig.suptitle(f"Couplings {name}", fontsize=16)

        if not plot:
            return fig, axis

        plt.show()

    def plot_detunings(self, plot: bool = True, name: str = "") -> Any:
        """Función que hace el plot de las funciones de las desintonizaciones con sus pares.

        Args:
            plot (bool, optional): Si se desea devolver la figura o no. Defaults to True.
            name (str, optional): Nombre del plot. Defaults to "".
            phase (bool, optional): Si se desea indicar las fases de los pulsos. Defaults to True.
            amp (bool, optional): Si se desea indicar las amplitudes de los pulsos. Defaults to True.

        Returns:
            Any: Figura del plot.
        """
        times = self.times
        p_pulses = {}

        pulse_config = self.backend_config.pulse_config
        detuning_color = pulse_config.DEFAULT_COLORS["detuning"]

        simulation_config = self.backend_config.simulation_config
        T_MAX = simulation_config.time_simulation

        for pulse in self.detuning_pulses.keys():
            pair = self.detuning_pulses[pulse][0]
            p_pulses[str(pair)] = []

        for key in self.detuning_pulses.keys():
            pair = self.detuning_pulses[key][0]
            pulse = self.detuning_pulses[key][-1]
            p_pulses[str(pair)].append(pulse)

        L = len(p_pulses.keys())
        fig, axis = plt.subplots(L, figsize=(16, 2 * L))

        for i in range(len(p_pulses.keys())):
            key = list(p_pulses.keys())[i]

            if len(p_pulses.keys()) == 1:
                for pulse in p_pulses[key]:
                    axis.plot(times, pulse, color=detuning_color[0])
                    axis.fill_between(times, pulse, color=detuning_color[0], alpha=0.3)
                    axis.set_ylabel(f"{key}")
                    axis.set_xlim(0, T_MAX)
            else:
                for pulse in p_pulses[key]:
                    axis[i].plot(times, pulse, color=detuning_color[i])
                    axis[i].fill_between(
                        times, pulse, color=detuning_color[i], alpha=0.3
                    )
                    axis[i].set_ylabel(f"{key}")
                    axis[i].set_xlim(0, T_MAX)

        fig.suptitle(f"Detunings {name}", fontsize=16)
        if not plot:
            return fig, axis

        plt.show()

    def plot_all(self):
        r"""Función que realiza el grafico de los acoples y las desintonizaciones."""
        self.plot_couplings()
        self.plot_detunings()


class RydbergRegisterSchedule:
    r"""Clase que contiene los parámetros del schedule dedicado para un registro de átomos."""

    def __init__(self, schedules: List[RydbergQubitSchedule], **kwargs):
        if "backend" in kwargs:
            backend_config = kwargs["backend"]
            assert isinstance(backend_config, BackendConfig)

            self.backend_config = backend_config

        else:
            self.backend_config = None

        simulation_config = self.backend_config.simulation_config
        sampling = simulation_config.sampling
        bitdepth = simulation_config.bitdepth
        t_max = simulation_config.time_simulation

        self.schedules = schedules
        self.times = aqipt.general_params(
            {"sampling": sampling, "bitdepth": bitdepth, "time_dyn": t_max}
        ).timebase()
        self.n_qubits = len(schedules)

    def plot_schedule(self, couplings=True, detunings=False):
        """Función que genera los graficos de todos los schedules del registro.

        Args:
            couplings (bool, optional): Si se desean ver los acoples. Defaults to True.
            detunings (bool, optional): Si se desean ver las desintonizaciones. Defaults to False.
        """
        for i, schedule in enumerate(self.schedules):
            if couplings:
                schedule.plot_couplings(name=f" {i}")

            if detunings:
                schedule.plot_detunings(name=f" {i}")
