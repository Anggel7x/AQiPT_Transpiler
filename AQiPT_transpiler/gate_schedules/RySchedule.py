from typing import Optional
import numpy as np
from ..gate_schedules.UxySchedule import UxySchedule


class RySchedule(UxySchedule):
    r"""Este es el schedule para la compurta Ry. 
    
    **Representación matricial:**

    .. math::
        R_{y}(\theta)_{\mathfrak{R}} = U_{x,y}(\theta, -\pi/2) = 
        \begin{pmatrix}
            \cos\qty(\frac{\theta}{2}) & \sin\qty(\frac{\theta}{2}) \\
            -\sin\qty(\frac{\theta}{2}) & \cos\qty(\frac{\theta}{2})
        \end{pmatrix}.

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
        super().__init__(theta, -np.pi / 2, t_start, freq, shape, pair, **kwargs)

    def _schedule(self):
        Ry = UxySchedule(
            self.theta,
            -np.pi / 2,
            self.t_start,
            self.freq,
            self.shape,
            backend=self.backend_config,
        )
        self.t_end = Ry.t_end
        self.q_schedule = Ry.q_schedule
        return Ry
