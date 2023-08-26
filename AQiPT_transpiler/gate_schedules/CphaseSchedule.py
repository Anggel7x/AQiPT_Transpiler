from typing import Optional
import numpy as np
from ..gate_schedules.GateSchedule import GateSchedule
from ..gate_schedules.RxSchedule import RxSchedule
from ..utils.schedules_utils import freq_given_phi


class CphaseSchedule(GateSchedule):
    r"""Este es el schedule ede la compuerta diagonal que introduce una fase en el estado del 
    qubit objetivo dependiento del estado del control, llamda CPHASE.

    **Representación matricial:**

    .. math::

        \text{CPHASE}(\Phi_{11}) =
            \begin{pmatrix}
                1 & 0 & 0 & 0 \\
                0 & -1 & 0 & 0 \\
                0 & 0 & -1 & 0 \\
                0 & 0 & 0 & e^{i\Phi_{11}}
            \end{pmatrix}

    **Operador evolución:**

    .. math::
        
        \begin{split}
            \hat{U} = &\exp\qty[-i\hat{H}^{r1}_c(\Omega=\Omega_1,\Delta=0)\tau_1] \\
                &\cross \exp\qty[-i\qty(\hat{H}^{r1}_t(\Omega=\Omega_2, \Delta=0) + \hat{H}^{rrrr}_{c,t})\tau_2] \\
                &\cross \exp\qty[-i\hat{H}^{r1}_c(\Omega=\Omega_1,\Delta=0)\tau_1] 
        \end{split}    

    
    """

    def __init__(
        self,
        t_start: float = 1,
        phi11: float = 0,
        freq: float = 1,
        pair: Optional[list] = None,
        shape: str = "gaussian",
        **kwargs
    ) -> None:
        if pair is None:
            pair = [[1, 3], [1, 3]]
        super().__init__(t_start, freq, pair, shape, **kwargs)

        self.phi11 = phi11

        self._schedule()

    def _schedule(self):
        t_start = self.t_start
        freq = self.freq
        shape = self.shape
        c_pair, t_pair = self.pair[0], self.pair[1]

        atomic_config = self.backend_config.atomic_config
        c_6 = atomic_config.c6_constant
        r_dist = atomic_config.R
        v_ct = c_6 / np.power(r_dist, 6)

        freq_int = freq_given_phi(self.phi11, v_ct)

        # 1 -> r
        rc1 = RxSchedule(
            theta=np.pi,
            t_start=t_start,
            freq=freq,
            shape=shape,
            pair=c_pair,
            backend=self.backend_config,
        )

        # r -> r
        rt1 = RxSchedule(
            theta=2 * np.pi,
            t_start=rc1.t_end,
            freq=freq_int,
            shape="gaussian",
            pair=t_pair,
            backend=self.backend_config,
        )
        # r -> 1
        rc2 = RxSchedule(
            theta=np.pi,
            t_start=rt1.t_end,
            freq=freq,
            shape=shape,
            pair=c_pair,
            backend=self.backend_config,
        )

        rc1.q_schedule.add_function(
            rc2.q_schedule.coupling_pulses["Coupling0"][2], "Coupling0"
        )

        self.t_end = rc2.t_end

        self.q_schedule = (rc1, rt1)  # control and target schedules
