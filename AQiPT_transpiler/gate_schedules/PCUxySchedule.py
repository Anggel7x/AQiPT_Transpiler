from ..rydberg_blocks.shaped_pulses import *
from ..rydberg_blocks.rydberg_qubits import *
from ..gate_schedules.GateSchedule import GateSchedule
from ..gate_schedules.UxySchedule import UxySchedule


class PCUxySchedule(GateSchedule):
    def __init__(
        self,
        theta: float = np.pi,
        phi: float = 0,
        t_start: float = 1,
        freq: float = 1,
        shape: str = "square",
        pair: list = [0, 1],
        **kwargs
    ) -> None:
        super().__init__(t_start, freq, pair, shape, **kwargs)

        self.theta = theta
        self.phi = phi

        self._schedule()

    def _schedule(self):
        target_schedule = UxySchedule(
            theta=self.theta,
            phi=self.phi,
            t_start=self.t_start,
            freq=self.freq,
            shape=self.shape,
            backend=self.backend_config,
        )

        control_schedule = UxySchedule(
            theta=self.theta,
            phi=self.phi,
            t_start=self.t_start,
            freq=self.freq,
            shape=self.shape,
            backend=self.backend_config,
        )

        self.t_end = target_schedule.t_end
        self.q_schedule = (target_schedule, control_schedule)