from transpiler.rydberg_blocks.shaped_pulses import *
from transpiler.rydberg_blocks.rydberg_qubits import *
from transpiler.gate_schedules.GateSchedule import *
from transpiler.gate_schedules.RxSchedule import RxSchedule
from transpiler.utils.schedules_utils import freq_given_phi


class CphaseSchedule(GateSchedule):
    
    def __init__(self, 
                 t_start : float = 1, 
                 phi11: float = 0,
                 freq: float = 1, 
                 pair: list = [[1,3], [1,3]],
                 shape: str = "gaussian",
                 **kwargs) -> None:
        
        super().__init__(t_start, freq, pair, shape, **kwargs)
        
        self.phi11 = phi11
        
        self._schedule()    

    def _schedule(self):
        
        t_start = self.t_start
        freq = self.freq
        shape = self.shape
        c_pair, t_pair = self.pair[0], self.pair[1]
        
        atomic_config = self.backend_config.atomic_config
        C6 = atomic_config.c6_constant
        R = atomic_config.R
        Vct = C6/np.power(R, 6)
        
        freq_int = freq_given_phi(self.phi11, Vct)
        
        # 1 -> r
        rc1 = RxSchedule(theta=np.pi, t_start=t_start, freq=freq, shape=shape, pair=c_pair, backend=self.backend_config)

        # r -> r 
        r2 = RxSchedule(theta=2*np.pi,t_start=rc1.t_end, freq=freq_int, shape=shape, pair=t_pair, backend=self.backend_config)

        # r -> 1
        rc2 = RxSchedule(theta=np.pi, t_start=r2.t_end, freq=freq, shape=shape, pair=c_pair, backend=self.backend_config)

        rc1.q_schedule.add_function(rc2.q_schedule.coupling_pulses["Coupling0"][2], "Coupling0")
        
        self.t_end = rc2.t_end
        
        self.q_schedule = (rc1, r2) # control and target schedules
