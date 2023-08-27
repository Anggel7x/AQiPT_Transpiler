import numpy as np
from ..rydberg_blocks.shaped_pulses import CERO_FUNCTION
from ..rydberg_blocks.rydberg_qubits import RydbergQubitSchedule
from ..config.core import default_backend, BackendConfig


class GateSchedule:
    def __init__(
        self, t_start: float, freq: float, pair: list, shape: str, **kwargs
    ) -> None:
        r"""Clase que contiene las bases fundamentales del schedule de una compuerta.

        Args:
            t_start (float): Tiempo de inicio del schedule.
            freq (float): Frecuencia normal para los pulsos dentro del schedule.
            pair (list): Par de estados necesarios paral el schedule.
            shape (str): Forma normal de los pulsos dentro del schedule.
        """
        self.t_start = t_start
        self.t_end = t_start
        self.freq = freq
        self.pair = pair
        self.shape = shape
        self.n_qubits = len(pair)
        self.omega = 2 * np.pi * freq
        self.q_schedule = None

        if "backend" in kwargs.keys():
            backend_config = kwargs["backend"]
            assert isinstance(backend_config, BackendConfig)

            self.backend_config = backend_config

        else:
            self.backend_config = default_backend

    def __call__(self):
        return self.q_schedule


def CeroSchedule() -> RydbergQubitSchedule:
    """Definición del schedule de valor nulo.

    Returns:
        RydbergQubitSchedule: Retorno del schedule.
    """
    couplings = [
        ([0, 1], CERO_FUNCTION.function),
    ]

    detunings = [([1, 1], CERO_FUNCTION.function)]

    coupling1 = {}
    for i, coupling in enumerate(couplings):
        levels, coupling = coupling
        coupling1["Coupling" + str(i)] = [levels, 0, coupling]

    detuning1 = {}
    for i, detuning in enumerate(detunings):
        levels, detuning = detuning
        detuning1["Detuning" + str(i)] = [levels, 0, detuning]

    return RydbergQubitSchedule(coupling_pulses=coupling1, detuning_pulses=detuning1)
