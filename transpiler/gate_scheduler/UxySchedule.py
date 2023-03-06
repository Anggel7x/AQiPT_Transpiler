from transpiler.aqipt_pulses import *
from transpiler.rydberg_circuits import *

def coupling_detuning_constructors(couplings: List, detunings : List, omega_coup : 20, omega_detu = 0) -> tuple():
    coupling1 = {}
    for i, coupling in enumerate(couplings):
        levels , coupling = coupling
        coupling1['Coupling'+str(i)] = [levels, omega_coup, coupling]


    detuning1 = {}
    for i, detuning in enumerate(detunings):
        levels , detuning = detuning
        detuning1['Detuning'+str(i)] = [levels, omega_detu, detuning]
        
    return coupling1, detuning1

class UxySchedule():
    
    def __init__(self,
                 theta: float = np.pi, 
                 phi: float = 0, 
                 t_start : float = 1, 
                 freq: float = 1, 
                 shape: str = "square") -> None:
        
        self.theta = theta
        self.phi = phi
        self.t_start = t_start
        self.freq = freq
        self.shape = shape
        
        self._schedule()    

    def _schedule(self):
        omega = 2*np.pi*self.freq
        self.omega = omega
        
        if self.shape == "square":
            pulse_1 = SquarePulse(t_start=self.t_start, area=self.theta/omega)
            complx_pulse_1 = pulse_1.function*np.exp(+1j*2*self.phi*pulse_1.function)
        elif self.shape == "gaussian":
            pulse_1 = GaussianPulse(t_start=self.t_start, area=self.theta/omega)
            pulse_t1 = SquarePulse(t_start=pulse_1.t_start, t_end=pulse_1.t_end)
            complx_pulse_1 = pulse_1.function*np.exp(+1j*2*self.phi*pulse_t1.function)

        self.t_end = pulse_1.t_end
        coupling = [
            ([0,1], complx_pulse_1)
        ]
        
        detuning = [
            ([1,1], CERO_FUNCTION.function)
        ]
        
        coup, detun = coupling_detuning_constructors(coupling, detuning, omega_coup=omega)
        qubit_schedule1 = RydbergQubitSchedule(coupling_pulses=coup, detuning_pulses=detun)
        
        self.q_schedule = qubit_schedule1
        return qubit_schedule1

    def __call__(self):
        return self.q_schedule