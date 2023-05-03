from transpiler.aqipt_pulses import *
from transpiler.rydberg_circuits import *
from .GateSchedule import *
from transpiler.gate_scheduler.UxySchedule import UxySchedule

class CUxySchedule(GateSchedule):
    
    def __init__(self,
                 theta: float = np.pi, 
                 phi: float = 0, 
                 t_start : float = 1, 
                 freq: float = 1, 
                 pair: list = [[0,1], [0,1]],
                 shape: str = "square") -> None:
        
        super().__init__(t_start, freq, pair)
        
        self.theta = theta
        self.phi = phi
        self.shape = shape
        
        self._schedule()    

    def _schedule(self):
        target_schedule = UxySchedule(theta=self.theta, 
                                            phi=self.phi,
                                            t_start=self.t_start, 
                                            freq=self.freq, 
                                            pair=self.pair[0],
                                            shape=self.shape)
        control_schedule = UxySchedule(
                                        theta=0,
                                        t_start=self.t_start, 
                                        freq=self.freq, 
                                        pair=self.pair[0],
                                        shape=self.shape
                                    )
        
        self.t_end = target_schedule.t_end
        self.q_schedule = (control_schedule, target_schedule)

    