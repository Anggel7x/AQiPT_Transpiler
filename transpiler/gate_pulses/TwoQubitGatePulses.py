from ..aqipt_pulses import *
from ..rydberg_circuits import RydbergQubitSchedule
from typing import List

class TwoQubitGatePulses():
    
    def __init__(
        self, 
        name: str, 
        params: dict,
        t_o: List[float],
        times = PULSE_PARAMS.timebase(),
        shape = 'Gaussian',
    ):
        self.name = name
        self.qubits = 2
        self.params = params
        self.times = times
        self.shape = shape
        self.omega = params['omega']
        self.omega_dt = params['omega_dt']
        self.t_o = [t_o, None] # Center time of the first pulse
        
        self.t_i = [] # Initial time of the schedule
        self.t_f = [] # Final time of the schedule
        self.t_s = [] # Total time of the schedule
        
        self.t_e = [] # Center time of the last pulse
        self.t_d = [] # Total time between central times of
        
        self.couplings = []
        self.detunings = []
        self.schedules = [] 
        
        self.ncouplings = []
        self.ndetunings = []
        self.npulses = []
        
        # constant strings
        self.TG = ()
        self.TS = ()
    
    def _time_constants(self):
        omega = self.omega
        # Gaussian Pulses standar durations constants
        TG90 = X90GaussianPulse(t_o=1, omega=omega).tg/2;
        TG180 = X180GaussianPulse(t_o=1, omega=omega).tg/2;

        TG0 = 2*TG90
        TG1 = TG90 + TG180
        TG2 = 2*TG180
    
        self.TG = (TG0, TG1, TG2)
        
        # Square Pulses standar durations constants
        TS90 = X90SquarePulse(t_o=1, omega=omega).tg/2;
        TS180 = X180SquarePulse(t_o=1, omega=omega).tg/2;

        TS0 = 2*TS90
        TS1 = TS90 + TS180
        TS2 = 2*TS180

        self.TS = (TS0, TS1, TS2)

    
    def _number_params_lst(self):
        
        for coupling in self.couplings:
            self.ncouplings.append(len(coupling))

        for detuning in self.detunings:
            self.ndetunings.append(len(detuning))

        for i in range(2):
            self.npulses.append( self.ncouplings[i] + self.ndetunings[i] )

    
    def _time_params_lst(self):

        self.t_o = [coupling[0][1].t_o for coupling in  self.couplings]

        for i in range(len(self.couplings)):
            couplings = self.couplings[i]
            first_pulse = couplings[0][1]
            last_pulse = couplings[-1][1]
            
            self.t_e.append(last_pulse.t_o)
            self.t_d.append(self.t_e[i] - self.t_o[i])
            
            self.t_i.append(self.t_o[i] - first_pulse.tg/2)
            self.t_f.append(self.t_e[i] + last_pulse.tg/2)
            self.t_s.append(self.t_f[i] - self.t_i[i])
            


    