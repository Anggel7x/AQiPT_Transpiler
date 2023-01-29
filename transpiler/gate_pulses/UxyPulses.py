from .OneQubitGatePulses import *

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
     