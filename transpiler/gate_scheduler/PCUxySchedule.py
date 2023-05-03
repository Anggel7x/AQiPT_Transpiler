from transpiler.aqipt_pulses import *
from transpiler.rydberg_circuits import *
from transpiler.gate_scheduler.UxySchedule import UxySchedule

class PCUxySchedule(UxySchedule):
    
    def __init__(self,
                 theta: float = np.pi, 
                 phi: float = 0, 
                 t_start : float = 1, 
                 freq: float = 1, 
                 shape: str = "square",
                 pair: list = [0,1]) -> None:
        
        super().__init__(theta, phi, t_start, freq, shape, pair)
        
        self._schedule()    

    def _schedule(self):
        target_schedule = UxySchedule(theta=self.theta, 
                                            phi=self.phi,
                                            t_start=self.t_start, 
                                            freq=self.freq, 
                                            shape=self.shape)
        
        
        control_schedule = UxySchedule(theta=self.theta, 
                                            phi=self.phi,
                                            t_start=self.t_start, 
                                            freq=self.freq, 
                                            shape=self.shape)
        
        self.t_end = target_schedule.t_end
        self.q_schedule = (target_schedule, control_schedule)