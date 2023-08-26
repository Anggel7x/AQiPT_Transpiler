from typing import Optional
import numpy as np
from ..gate_schedules.UxySchedule import UxySchedule


class RzSchedule(UxySchedule):
    r"""Este es el schedule para la compurta Rz. 
    
    **Representación matricial:**

    .. math::
        R_z(\theta)_\mathfrak{R} = U_{x,y}(\pi/2,\pi/2)U_{x,y}(\theta,0)U_{x,y}(\pi/2, -\pi/2) = \begin{pmatrix}
            e^{i\theta/2} & 0 \\
            0 & e^{-i\theta/2}
        \end{pmatrix} = R_z(-\theta)

    """

    def __init__(
        self,
        theta: float = np.pi,
        t_start: float = 1,
        freq: float = 1,
        shape: str = "square",
        pair: Optional[list] = None,
        **kwargs
    ) -> None:
        if pair is None:
            pair = [0, 1]
        super().__init__(theta, 0, t_start, freq, shape, pair, **kwargs)

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
