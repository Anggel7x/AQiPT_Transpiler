from transpiler.aqipt_pulses import *
from transpiler.rydberg_circuits import *
from .UxySchedule import UxySchedule


class RySchedule(UxySchedule):
    
    def __init__(self,
                 theta: float = np.pi, 
                 t_start : float = 1, 
                 freq: float = 1, 
                 shape: str = "square") -> None:
        
        super().__init__(theta, -np.pi/2, t_start, freq, shape)  

    def _schedule(self):
        
        Ry = UxySchedule(self.theta, -np.pi/2, self.t_start, self.freq, self.shape)
        self.q_schedule = Ry.q_schedule
        return Ry