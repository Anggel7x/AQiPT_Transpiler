from .TwoQubitGatePulses import *

class CPhaseGatePulses(TwoQubitGatePulses):

    def __init__(
        self, 
        omega: float,
        omega_dt: float,
        c6: int,
        phi11: float,
        t_o: float, 
        times = PULSE_PARAMS.timebase(), 
        shape = 'Gaussian'):

        params = {'omega':omega, 'omega_dt': omega_dt, 'phi11':phi11, 'c6' : c6}
        super().__init__('CPhase', params, t_o, times, shape)

        self._time_constants()
        self._define()
        self._number_params_lst()
        self._time_params_lst()          

    def tg_for_c6(self, t, c6, r=1):
        return (t*(r**6))/(2*np.pi*c6)

    def _define(self):
        omega = self.omega
        omega_dt = self.omega_dt

        phi11 = self.params['phi11']
        c6 = self.params['c6']

        if self.shape == 'Gaussian': 
            MainPulse = GaussianPulse 
            T0, T1, T2 = self.TG
        elif self.shape == 'Square':
            MainPulse = SquarePulse
            T0, T1, T2 = self.TS

        # Pulses Construction
        t0 = self.t_o[0]
        pulse_0 = MainPulse(t_o = t0, area=np.pi, omega = omega) #Pi Pulse
    
        t1 = t0 + T2 + self.tg_for_c6(phi11, c6, 1)
        pulse_1 = MainPulse(t_o = t1, area=np.pi,  omega=omega)

        couplings = [
            ( [0,2] , pulse_0),
            ( [2,0] , pulse_1)
        ]
        
        detunings = [
            ( [1,1], CERO_FUNCTION),
        ]

        coupling1 = {}
        for i in range(len(couplings)):
            levels , coupling = couplings[i]
            coupling1['Coupling'+str(i)] = [levels, 2*np.pi*omega, coupling.function]
            
        detuning1 = {}
        for i in range(len(detunings)):
            levels , coupling = detunings[i]
            detuning1['Detuning'+str(i)] = [levels, -2*np.pi*omega_dt, coupling.function]
        
        self.couplings = [couplings, couplings]
        self.detunings = [detunings, detunings]

        schedule  = RydbergQubitSchedule(coupling1, detuning1, self.times)
        self.schedules = [schedule, schedule]
        