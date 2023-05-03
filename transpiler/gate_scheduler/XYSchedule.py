from transpiler.aqipt_pulses import *
from transpiler.rydberg_circuits import *
from .GateSchedule import *
from transpiler.gate_scheduler.RxSchedule import RxSchedule

class XYSchedule(GateSchedule):
    
    def __init__(self, 
                 t_start : float = 1, 
                 t_2: float = 0,
                 freq: float = 1, 
                 pair: list = [[0,2], [1,3]],
                 shape: str = "square") -> None:
        
        super().__init__(t_start, freq, pair)
        
        self.t_2 = t_2
        self.shape = shape
        
        self._schedule()    

    def _schedule(self):
        
        t_start = self.t_start
        freq = self.freq
        shape = self.shape
        t2 = self.t_2
        omega = self.omega

        
        if shape == "square":
            ShapedPulse = SquarePulse
        elif shape == "gaussian":
            ShapedPulse = GaussianPulse
        else:
            raise ValueError(f"{shape} is not a valid shape")
        
        
        # pi 0 -> r 0 phase [0, 2]
        rc1 = ShapedPulse(t_start=t_start, area=np.pi/omega) # control

        # 2pi 1 -> r' 0 phase [1, 3]
        rc2 = ShapedPulse(t_start=rc1.t_end, t_end=rc1.t_end+t2, amp=2*np.pi/t2)

        # 2pi 1 -> r' pi phase [1, 3]
        rc3_a = ShapedPulse(t_start=rc2.t_end, t_end=rc2.t_end+t2, amp=2*np.pi/t2)
        rc3_p = SquarePulse(t_start=rc3_a.t_start, t_end=rc3_a.t_end)
        rc3 = rc3_a.function*np.exp(+1j*2*np.pi*rc3_p.function)

        # pi r -> 0 pi phase [0, 2]
        rc4_a = ShapedPulse(t_start=rc3_a.t_end, area=np.pi/omega)
        rc4_p = SquarePulse(t_start=rc4_a.t_start, t_end=rc4_a.t_end)
        rc4 = rc4_a.function*np.exp(+1j*2*np.pi*rc4_p.function)
            

        t_end = rc4_a.t_end
        self.t_end = t_end
        
        p, q = self.pair[0], self.pair[1]
        couplings = [
            (p, rc1.function),
            (q, rc2.function),
            (q, rc3),
            (p, rc4)
        ]

        detuning = [
                    ([1,1], CERO_FUNCTION.function)
                ]

        coup, detun = coupling_detuning_constructors(couplings, detuning, omega_coup=omega)
        qubit_schedule = RydbergQubitSchedule(coupling_pulses=coup, detuning_pulses=detun)
        
        self.q_schedule = (qubit_schedule, qubit_schedule) # control and target schedules

