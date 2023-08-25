import numpy as np
from ..gate_schedules.GateSchedule import GateSchedule
from ..gate_schedules.UxySchedule import UxySchedule
from ..gate_schedules.RxSchedule import RxSchedule


class CUxySchedule(GateSchedule):
    def __init__(
        self,
        theta: float = np.pi,
        phi: float = 0,
        t_start: float = 1,
        freq: float = 1,
        pair: list = [[1, 3], [0, 3]],
        shape: str = "square",
        **kwargs
    ) -> None:
        super().__init__(t_start, freq, pair, shape)

        self.theta = theta
        self.phi = phi

        self._schedule()

    def _schedule(self):
        r1 = RxSchedule(
            theta=np.pi,
            t_start=self.t_start,
            freq=self.freq,
            shape=self.freq,
            pair=self.pair[0],
            backend=self.backend_config,
        )

        r2 = UxySchedule(
            theta=self.theta,
            phi=self.phi,
            t_start=r1.t_end,
            freq=self.freq,
            pair=self.pair[1],
            shape=self.shape,
            backend=self.backend_config,
        )

        r3 = RxSchedule(
            theta=np.pi,
            t_start=r2.t_end,
            freq=self.freq,
            pair=self.pair[0],
            shape=self.shape,
            backend=self.backend_config,
        )

        r1.q_schedule.add_function(
            r2.q_schedule.coupling_pulses["Coupling0"][2], "Coupling0"
        )
        r1.q_schedule.add_function(
            r3.q_schedule.coupling_pulses["Coupling0"][2], "Coupling0"
        )
        target_schedule = r1

        control_schedule = UxySchedule(
            theta=0,
            t_start=self.t_start,
            freq=self.freq,
            pair=self.pair[0],
            shape=self.shape,
            backend=self.backend_config,
        )

        self.t_end = target_schedule.t_end
        self.q_schedule = (control_schedule, target_schedule)
