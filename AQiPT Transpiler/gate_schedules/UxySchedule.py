from ..rydberg_blocks.shaped_pulses import *
from ..rydberg_blocks.rydberg_qubits import *
from ..gate_schedules.GateSchedule import GateSchedule
from ..utils.schedules_utils import coupling_detuning_constructors


class UxySchedule(GateSchedule):
    
    def __init__(self,
                 theta: float = np.pi, 
                 phi: float = 0, 
                 t_start : float = 1, 
                 freq: float = 1, 
                 shape: str = "square",
                 pair: list = [0,1],
                 **kwargs) -> None:
        
        super().__init__(t_start, freq, pair, shape, **kwargs)
        self.theta = theta
        self.phi = phi
        
        self._schedule()    

    def _schedule(self) -> RydbergQubitSchedule:
        omega = 2*np.pi*self.freq
        self.omega = omega
        if self.shape == "square":
            ShapedPulse = SquarePulse
        elif self.shape == "gaussian":
            ShapedPulse = GaussianPulse
        else:
            raise ValueError(f"{self.shape} is not a valid shape.")
        
        
        pulse_1 = ShapedPulse(t_start=self.t_start, area=self.theta/omega, backend=self.backend_config)
        
        pulse_t1 = SquarePulse(t_start=self.t_start, t_end=pulse_1.t_end, backend=self.backend_config)
        complx_pulse_1 = pulse_1.function*np.exp(-1j*self.phi*pulse_t1.function)
            
        self.t_end = pulse_1.t_end
        
        coupling = [
            (self.pair, complx_pulse_1)
        ]
        
        detuning = [
            ([1,1], CERO_FUNCTION.function)
        ]
        
        coup, detun = coupling_detuning_constructors(coupling, detuning, omega_coup=omega)
        qubit_schedule1 = RydbergQubitSchedule(coupling_pulses=coup, detuning_pulses=detun, backend=self.backend_config)
        
        self.q_schedule = qubit_schedule1
        return qubit_schedule1