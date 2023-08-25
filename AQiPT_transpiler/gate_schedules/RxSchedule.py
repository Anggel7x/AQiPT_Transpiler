from ..rydberg_blocks.shaped_pulses import *
from ..rydberg_blocks.rydberg_qubits import *
from ..gate_schedules.UxySchedule import UxySchedule


class RxSchedule(UxySchedule):
    def __init__(
        self,
        theta: float = np.pi,
        t_start: float = 1,
        freq: float = 1,
        shape: str = "square",
        pair: list = [0, 1],
        **kwargs
    ) -> None:
        super().__init__(theta, 0, t_start, freq, shape, pair, **kwargs)

    def _schedule(self):
        Rx = UxySchedule(
            self.theta,
            0,
            self.t_start,
            self.freq,
            self.shape,
            self.pair,
            backend=self.backend_config,
        )
        self.t_end = Rx.t_end
        self.q_schedule = Rx.q_schedule
        return Rx
