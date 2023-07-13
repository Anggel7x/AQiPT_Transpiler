from transpiler.aqipt_pulses import *
from transpiler.rydberg_circuits import *
from .GateSchedule import *
from transpiler.gate_schedules.RxSchedule import RxSchedule

class CZSchedule(GateSchedule):
    
    def __init__(self, 
                 t_start : float = 1, 
                 freq: float = 1, 
                 pair: list = [[1,2], [1,2]],
                 shape: str = "square") -> None:
        
        super().__init__(t_start, freq, pair)
        
        self.shape = shape
        
        self._schedule()    

    def _schedule(self):
        
        t_start = self.t_start
        freq = self.freq
        shape = self.shape
        c_pair, t_pair = self.pair[0], self.pair[1]
        
        # 1 -> r
        rc1 = RxSchedule(theta=np.pi, t_start=t_start, freq=freq, shape=shape, pair=c_pair)

        # Interacción durante t2
        r2 = RxSchedule(theta=2*np.pi,t_start=rc1.t_end, freq=freq, shape=shape, pair=t_pair)

        # r -> 1
        rc2 = RxSchedule(theta=np.pi, t_start=r2.t_end, freq=freq, shape=shape, pair=c_pair)

        rc1.q_schedule.add_function(rc2.q_schedule.coupling_pulses["Coupling0"][2], "Coupling0")
        
        self.q_schedule = (rc1, r2) # control and target schedules