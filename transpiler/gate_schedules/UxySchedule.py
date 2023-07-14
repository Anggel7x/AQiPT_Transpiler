from transpiler.rydberg_blocks.shaped_pulses import *
from transpiler.rydberg_blocks.rydberg_qubits import *
from .GateSchedule import GateSchedule, coupling_detuning_constructors

class UxySchedule(GateSchedule):
    
    def __init__(self,
                 theta: float = np.pi, 
                 phi: float = 0, 
                 t_start : float = 1, 
                 freq: float = 1, 
                 shape: str = "square",
                 pair: list = [0,1]) -> None:
        
        super().__init__(t_start, freq, pair, shape)
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
        
        _theta = self.theta
        while (_theta/omega < np.pi/8 and _theta != 0):
            _theta += 2*np.pi
        
        pulse_1 = ShapedPulse(t_start=self.t_start, area=_theta/omega)
        
        pulse_t1 = SquarePulse(t_start=self.t_start, t_end=pulse_1.t_end)
        complx_pulse_1 = pulse_1.function*np.exp(-1j*self.phi*pulse_t1.function)
            
        self.t_end = pulse_1.t_end
        
        coupling = [
            (self.pair, complx_pulse_1)
        ]
        
        detuning = [
            ([1,1], CERO_FUNCTION.function)
        ]
        
        coup, detun = coupling_detuning_constructors(coupling, detuning, omega_coup=omega)
        qubit_schedule1 = RydbergQubitSchedule(coupling_pulses=coup, detuning_pulses=detun)
        
        self.q_schedule = qubit_schedule1
        return qubit_schedule1