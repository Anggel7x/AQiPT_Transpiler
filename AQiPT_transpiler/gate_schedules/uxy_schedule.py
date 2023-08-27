from typing import Optional
import numpy as np
from ..rydberg_blocks.shaped_pulses import SquarePulse, GaussianPulse
from ..rydberg_blocks.rydberg_qubits import RydbergQubitSchedule
from .gate_schedule import GateSchedule, CERO_FUNCTION
from ..utils.schedules_utils import coupling_detuning_constructors


class UxySchedule(GateSchedule):
    r"""Este es el schedule para la compuerta XY en átomos de Rydberg.
    
    **Representación matricial:**

    .. math::

        U_{xy}(\theta, \varphi) = 
        \qty(\begin{array}{cc}
         \cos{(\theta/2)} & -i \sin{(\theta/2)e^{-i\varphi}  }  \\
         -i \sin{(\theta/2)e^{+i\varphi}} & \cos{(\theta/2)}, 
        \end{array})
    )

    **Operador evolución:**

    .. math::
        \hat{H}_j^{ab} = \qty(\frac{\Omega_j(t)}{2}e^{i\varphi_j(t)}\ket{a}\bra{b}+\text{h.c})  
        - \Delta_j(t)\ket{b}_j\bra{b}.
    """

    def __init__(
        self,
        theta: float = np.pi,
        phi: float = 0,
        t_start: float = 1,
        freq: float = 1,
        shape: str = "square",
        pair: Optional[list] = None,
        **kwargs,
    ) -> None:
        if pair is None:
            pair = [0, 1]
        super().__init__(t_start, freq, pair, shape, **kwargs)
        self.theta = theta
        self.phi = phi

        self._schedule()

    def _schedule(self) -> RydbergQubitSchedule:
        omega = 2 * np.pi * self.freq
        self.omega = omega
        if self.shape == "square":
            ShapedPulse = SquarePulse
        elif self.shape == "gaussian":
            ShapedPulse = GaussianPulse
        else:
            raise ValueError(f"{self.shape} is not a valid shape.")

        pulse_1 = ShapedPulse(
            t_start=self.t_start, area=self.theta / omega, backend=self.backend_config
        )

        pulse_t1 = SquarePulse(
            t_start=self.t_start, t_end=pulse_1.t_end, backend=self.backend_config
        )
        complx_pulse_1 = pulse_1.function * np.exp(-1j * self.phi * pulse_t1.function)

        self.t_end = pulse_1.t_end

        coupling = [(self.pair, complx_pulse_1)]

        detuning = [([1, 1], CERO_FUNCTION.function)]

        coup, detun = coupling_detuning_constructors(
            coupling, detuning, omega_coup=omega
        )
        qubit_schedule1 = RydbergQubitSchedule(
            coupling_pulses=coup, detuning_pulses=detun, backend=self.backend_config
        )

        self.q_schedule = qubit_schedule1
        return qubit_schedule1
