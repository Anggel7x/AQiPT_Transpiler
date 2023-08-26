from typing import Optional
import numpy as np
from ..gate_schedules.UxySchedule import UxySchedule


class RxSchedule(UxySchedule):
    r"""Este es el schedule para la compuerta Rx. 
    
    **Representación matricial:**

    .. math::
        R_{x}(\theta)_{\mathfrak{R}} = U_{x,y}(\theta, 0) = 
        \begin{pmatrix}
            \cos\qty(\frac{\theta}{2}) & -i\sin\qty(\frac{\theta}{2}) \\
            -i\sin\qty(\frac{\theta}{2}) & \cos\qty(\frac{\theta}{2})
        \end{pmatrix},
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
