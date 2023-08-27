from typing import Optional
import numpy as np
from .gate_schedule import GateSchedule
from .uxy_schedule import UxySchedule


class PCUxySchedule(GateSchedule):
    r"""Este es el schedule para la compuerta pCUxy en átomos de Rydberg.

    **Representación matricial:**

    .. math::

        pCU_{xy} = \qty( 
        \begin{array}{c c c c}
            \cos{(\theta/2)} & s(\theta, \varphi) & s(\theta, \varphi) & 0  \\
            s(\theta, -\varphi) & \cos^2{(\theta/4)} & -\sin^2{(\theta/4)} & 0 \\
            s(\theta, -\varphi) & -\sin^2{(\theta/4)} & \cos^2{(\theta/4)} & 0 \\
            0 & 0 & 0 & 1 
        \end{array}
    ) 
    
    s(\theta, \varphi) = -i\sin{(\theta/2)e^{i\varphi}}/\sqrt{2}

    **Operador evolución:**

    .. math::
        
         \hat{U} = \exp{-i\qty(\hat{H}^{01}_c + \hat{H}^{01}_t + \hat{H}^{1111}_{c,t})\tau_g}.

    
    """

    def __init__(
        self,
        theta: float = np.pi,
        phi: float = 0,
        t_start: float = 1,
        freq: float = 1,
        shape: str = "square",
        pair: Optional[list] = None,
        **kwargs
    ) -> None:
        if pair is None:
            pair = [0, 1]
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
