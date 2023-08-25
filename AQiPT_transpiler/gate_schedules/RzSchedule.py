from ..rydberg_blocks.shaped_pulses import *
from ..rydberg_blocks.rydberg_qubits import *
from ..gate_schedules.UxySchedule import UxySchedule


class RzSchedule(UxySchedule):
    def __init__(
        self,
        theta: float = np.pi,
        t_start: float = 1,
        freq: float = 1,
        shape: str = "square",
        **kwargs
    ) -> None:
        super().__init__(theta, 0, t_start, freq, shape, **kwargs)

    def _schedule(self):
        Ry = UxySchedule(
            np.pi / 2,
            -np.pi / 2,
            t_start=self.t_start,
            freq=self.freq,
            shape=self.shape,
            backend=self.backend_config,
        )
        Rx = UxySchedule(
            self.theta,
            0,
            t_start=Ry.t_end,
            freq=self.freq,
            shape=self.shape,
            backend=self.backend_config,
        )
        R = UxySchedule(
            np.pi / 2,
            +np.pi / 2,
            t_start=Rx.t_end,
            freq=self.freq,
            shape=self.shape,
            backend=self.backend_config,
        )

        R.q_schedule.add_function(
            Rx.q_schedule.coupling_pulses["Coupling0"][2], "Coupling0"
        )
        R.q_schedule.add_function(
            Ry.q_schedule.coupling_pulses["Coupling0"][2], "Coupling0"
        )

        self.q_schedule = R.q_schedule
        self.t_end = R.t_end
        return R
