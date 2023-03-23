from transpiler.aqipt_pulses import *
from transpiler.rydberg_circuits import *
from .UxySchedule import UxySchedule

class RzSchedule(UxySchedule):
    
    def __init__(self,
                 theta: float = np.pi, 
                 t_start : float = 1, 
                 freq: float = 1, 
                 shape: str = "square") -> None:
        
        super().__init__(theta, 0, t_start, freq, shape)  

    def _schedule(self):
        
        Ry = UxySchedule(np.pi/2, -np.pi/2, t_start=self.t_start, shape=self.shape)
        Rx = UxySchedule(self.theta, 0, t_start=Ry.t_end, shape=self.shape)
        R = UxySchedule(np.pi/2, np.pi/2, t_start=Rx.t_end, shape=self.shape)
        
        R.q_schedule.add_function(Rx.q_schedule.coupling_pulses["Coupling0"][2], "Coupling0")
        R.q_schedule.add_function(Ry.q_schedule.coupling_pulses["Coupling0"][2], "Coupling0")
        
        self.q_schedule = R.q_schedule
        return R

   