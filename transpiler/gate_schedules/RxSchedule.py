from transpiler.aqipt_pulses import *
from transpiler.rydberg_circuits import *
from .UxySchedule import UxySchedule


class RxSchedule(UxySchedule):
    
    def __init__(self,
                 theta: float = np.pi, 
                 t_start : float = 1, 
                 freq: float = 1, 
                 shape: str = "square",
                 pair: list = [0,1]) -> None:
        
        super().__init__(theta, 0, t_start, freq, shape, pair)  

    def _schedule(self):
        Rx = UxySchedule(self.theta, 0, self.t_start, self.freq, self.shape, self.pair)
        self.t_end = Rx.t_end
        self.q_schedule = Rx.q_schedule
        return Rx