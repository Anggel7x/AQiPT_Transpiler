import numpy as np
from ..rydberg_blocks.shaped_pulses import GaussianPulse, SquarePulse
from ..rydberg_blocks.rydberg_qubits import RydbergQubitSchedule
from ..gate_schedules.GateSchedule import GateSchedule, CERO_FUNCTION
from ..utils.schedules_utils import coupling_detuning_constructors


class XYSchedule(GateSchedule):
    def __init__(
        self,
        theta: float = 3 * np.pi,
        t_start: float = 1,
        freq: float = 1,
        pair: list = [[0, 2], [1, 3]],
        shape: str = "square",
        **kwargs,
    ) -> None:
        super().__init__(t_start, freq, pair, shape, **kwargs)
        self.theta = theta
        self._schedule()

    def _schedule(self):
        theta = self.theta
        t_start = self.t_start
        freq = self.freq
        shape = self.shape
        c3 = self.backend_config.atomic_config.c3_constant
        R = self.backend_config.atomic_config.R
        Vct = c3 / (np.sqrt(R) ** 3)

        omega1 = 2 * np.pi * freq

        omega2 = (2 * np.pi / theta) * (-Vct)

        if shape == "square":
            ShapedPulse = SquarePulse
        elif shape == "gaussian":
            ShapedPulse = GaussianPulse
        else:
            raise ValueError(f"{shape} is not a valid shape")

        # 1: Pulse from 0 -> r at Omega 1, Pi pulse
        p1 = ShapedPulse(
            t_start=t_start, area=np.pi / omega1, backend=self.backend_config
        )

        # 2: Pulse from 1 -> r' at Omega 2, 2Pi Pulse
        p2 = SquarePulse(
            t_start=p1.t_end, area=2 * np.pi / omega2, backend=self.backend_config
        )

        # 3: Same as before but phase -Pi
        p3 = SquarePulse(
            t_start=p2.t_end * 1.2, area=2 * np.pi / omega2, backend=self.backend_config
        )
        p3_t = SquarePulse(
            t_start=p3.t_start, t_end=p3.t_end, backend=self.backend_config
        )
        p3_com = p3.function * np.exp(-1j * np.pi * p3_t.function)

        # 4: Same as first but phase -Pi
        p4 = ShapedPulse(
            t_start=p3.t_end, area=np.pi / omega1, backend=self.backend_config
        )
        p4_t = SquarePulse(
            t_start=p4.t_start, t_end=p4.t_end, backend=self.backend_config
        )
        p4_com = p4.function * np.exp(-1j * np.pi * p4_t.function)

        self.t_end = p4.t_end

        p, q = self.pair[0], self.pair[1]
        couplings = [(p, p1.function), (q, p2.function), (q, p3_com), (p, p4_com)]

        detuning = [([1, 1], CERO_FUNCTION.function)]

        coup, detun = coupling_detuning_constructors(
            couplings, detuning, omega_coup=[omega1, omega2, omega2, omega1]
        )
        qubit_schedule = RydbergQubitSchedule(
            coupling_pulses=coup, detuning_pulses=detun, backend=self.backend_config
        )

        self.q_schedule = (qubit_schedule, qubit_schedule)

        return (qubit_schedule, qubit_schedule)