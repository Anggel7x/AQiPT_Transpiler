from transpiler.aqipt_pulses import *
from transpiler.rydberg_circuits import *
from .GateSchedule import GateSchedule, coupling_detuning_constructors

class UxySchedule(GateSchedule):
    
    def __init__(self,
                 theta: float = np.pi, 
                 phi: float = 0, 
                 t_start : float = 1, 
                 freq: float = 1, 
                 shape: str = "square",
                 pair: list = [0,1]) -> None:
        
        super().__init__(t_start, freq, pair)
        self.theta = theta
        self.phi = phi
        self.shape = shape
        
        self._schedule()    

    def _schedule(self) -> RydbergQubitSchedule:
        omega = self.omega
        
        if self.shape == "square":
            pulse_1 = SquarePulse(t_start=self.t_start, area=self.theta/omega)
            pulse_t1 = SquarePulse(t_start=self.t_start, t_end=pulse_1.t_end)
            complx_pulse_1 = pulse_1.function*np.exp(+1j*2*self.phi*pulse_t1.function)
        elif self.shape == "gaussian":
            pulse_1 = GaussianPulse(t_start=self.t_start, area=self.theta/omega)
            pulse_t1 = SquarePulse(t_start=pulse_1.t_start, t_end=pulse_1.t_end)
            complx_pulse_1 = pulse_1.function*np.exp(+1j*2*self.phi*pulse_t1.function)

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