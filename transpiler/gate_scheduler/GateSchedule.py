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

class GateSchedule():
    
    def __init__(self,
                 t_start: float,
                 freq: float,
                 pair: list
                ) -> None:
        
        self.t_start = t_start
        self.t_end = t_start
        self.freq = freq
        self.pair = pair
        self.n_qubits = len(pair)
        self.omega = 2*np.pi*freq
        self.q_schedule = None
        
    def __call__(self):
        return self.q_schedule   
        
        
