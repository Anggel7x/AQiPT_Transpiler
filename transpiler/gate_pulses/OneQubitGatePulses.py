from ..aqipt_pulses import *
from ..rydberg_circuits import *

CERO_FUNCTION = SquarePulse(t_o = 0, amp=0)

# OneQubitGatePulses class

class OneQubitGatePulses():

    def __init__(
        self, 
        name: str, 
        params: dict,
        t_o: float,
        times = PULSE_PARAMS.timebase(),
        shape = 'Gaussian',
    ):
        self.name = name
        self.qubits = 1
        self.params = params
        self.times = times
        self.shape = shape
        self.omega = params['omega']
        self.omega_dt = params['omega_dt']
        self.t_o = t_o # Center time of the first pulse
        
        self.t_i = None # Initial time of the schedule
        self.t_f = None # Final time of the schedule
        self.t_s = None # Total time of the schedule
        
        self.t_e = None # Center time of the last pulse
        self.t_d = None # Total time between central times of
        
        self.couplings = None
        self.detunings = None
        self.schedule = {}
        
        self.ncouplings = None
        self.ndetunings = None
        self.npulses = None
        
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
    
  
    def _number_params(self, couplings, detunings):
        self.ncouplings = len(couplings)
        self.ndetunings = len(detunings)
        self.npulses = self.ncouplings + self.ndetunings
    
    
    def _time_params(self, couplings):
        
        first_pulse = couplings[0][1]
        last_pulse = couplings[-1][1]
        
        self.t_e = last_pulse.t_o
        self.t_d = self.t_e - self.t_o
        
        self.t_i = self.t_o - first_pulse.tg/2
        self.t_f = self.t_e + last_pulse.tg/2
        self.t_s = self.t_f - self.t_i
    

class UxyGatePulses(OneQubitGatePulses):
    def __init__(
        self, 
        omega: float,
        omega_dt: float,
        theta: float,
        t_o: float,
        phi: float = 0,
        times = PULSE_PARAMS.timebase(),
        shape = 'Gaussian',
        levels = [0,1]
    ):
        params = {'omega':omega, 'omega_dt': omega_dt,'theta':theta, 'phi':phi}
        super().__init__('Uxy', params, t_o, times, shape)
        self.levels = levels 
        
        self._time_constants()
        self._define()
        self._number_params(self.couplings, self.detunings)
        self._time_params(self.couplings)          
            
    def _define(self):
        omega = self.omega
        omega_dt = self.omega_dt
        
        theta = self.params['theta']
        phi = self.params['phi']
        
        
        if self.shape == 'Gaussian': 
            MainPulse = GaussianPulse 
        elif self.shape == 'Square':
            MainPulse = SquarePulse
        
        # Pulse Construction
        t_o = self.t_o
        
        pulse_0 = MainPulse(t_o = t_o, area = abs(theta), 
                            amp = +1 if theta >0 else -1, omega = omega)
        if phi != 0:
            pulse_dt0 = MainPulse(t_o = t_o, area = abs(phi), 
                                  amp = +1 if phi > 0 else -1, omega = omega_dt)
        else : pulse_dt0 = CERO_FUNCTION
        
        couplings = [
            ( self.levels , pulse_0),
        ]
        
        detunings = [
            ( [1,1], pulse_dt0),
        ]
        
        
        coupling1 = {}
        for i in range(len(couplings)):
            levels , coupling = couplings[i]
            coupling1['Coupling'+str(i)] = [levels, 2*np.pi*omega, coupling.function]
            
        detuning1 = {}
        for i in range(len(detunings)):
            levels , coupling = detunings[i]
            detuning1['Detuning'+str(i)] = [levels, -2*np.pi*omega_dt, coupling.function]
        
        self.couplings = couplings
        self.detunings = detunings
        self.schedule = RydbergQubitSchedule(coupling1, detuning1, self.times)
        
        











