from typing import Optional
import numpy as np
from .gate_schedule import GateSchedule
from .uxy_schedule import UxySchedule
from .rx_schedule import RxSchedule


class CUxySchedule(GateSchedule):
    r"""
    Este es el schedule de la versión controlada de CUxy. 
    
    **Representación matricial:**

    .. math::

        \newcommand{\th}{\frac{\theta}{2}}

        CU_{x,y}(\theta, \varphi)\ q_0, q_1 =
            U_{xy}(\theta,\varphi) \otimes |0\rangle\langle 0| +
            I \otimes |1\rangle\langle 1| =
        \begin{pmatrix}
            \cos{(\th)} & -i \sin{(\th)e^{-i\varphi}} & 0 & 0 \\
            -i\sin{(\th)e^{+i\varphi}} & \cos{(\th)} & 0 & 0 \\
            0 & 0 & 1 & 0 \\
            0 & 0 & 0 & 1 \\
        \end{pmatrix}
    
    **Operador evolución:**

    .. math::
        
        \hat{U} = \exp{-i\qty(\hat{H}^{01}_t+\hat{H}^{1111}_{c,t})\tau_g}.    

    """

    def __init__(
        self,
        theta: float = np.pi,
        phi: float = 0,
        t_start: float = 1,
        freq: float = 1.0,
        pair: Optional[list] = None,
        shape: str = "square",
        **kwargs
    ) -> None:
        if pair is None:
            pair = [[1, 3], [0, 3]]
        super().__init__(t_start, freq, pair, shape)

        self.theta = theta
        self.phi = phi

        self._schedule()

    def _schedule(self):
        r1 = RxSchedule(
            theta=np.pi,
            t_start=self.t_start,
            freq=self.freq,
            shape=self.shape,
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
