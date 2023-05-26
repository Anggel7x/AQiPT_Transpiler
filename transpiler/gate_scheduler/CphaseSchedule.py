from transpiler.aqipt_pulses import *
from transpiler.rydberg_circuits import *
from .GateSchedule import *
from transpiler.gate_scheduler.UxySchedule import UxySchedule
from transpiler.gate_scheduler.RxSchedule import RxSchedule

class CphaseSchedule(GateSchedule):
    
    def __init__(self, 
                 t_start : float = 1, 
                 t_2: float = 0,
                 freq: float = 1, 
                 pair: list = [[1,2], [1,2]],
                 shape: str = "square") -> None:
        
        super().__init__(t_start, freq, pair)
        
        self.t_2 = t_2
        self.shape = shape
        
        self._schedule()    

    def _schedule(self):
        
        t_start = self.t_start
        t_2 = self.t_2
        freq = self.freq
        shape = self.shape
        A = 1/2*(2*np.pi*freq)
        c_pair, t_pair = self.pair[0], self.pair[1]
            
        # 1 -> r
        rt1 = RxSchedule(theta=np.pi, t_start=t_start, freq=freq, shape=shape, pair=t_pair)
        rc1 = RxSchedule(theta=np.pi, t_start=t_start, freq=freq, shape=shape, pair=c_pair)

        # r -> 1 + t_2
        rt2 = UxySchedule(theta = A, t_start=rt1.t_end + t_2, freq=freq, shape=shape, pair=t_pair)
        rc2 = UxySchedule(theta = A, t_start=rc1.t_end + t_2, freq=freq, shape=shape, pair=c_pair)

        self.t_end = rt2.t_end
        
        rt1.q_schedule.add_function(rt2.q_schedule.coupling_pulses["Coupling0"][2], "Coupling0")
        rc1.q_schedule.add_function(rc2.q_schedule.coupling_pulses["Coupling0"][2], "Coupling0")
        self.q_schedule = (rc1, rt1) # control and target schedules
