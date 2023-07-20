from typing import List, Dict, Any, Union
from pydantic_settings import BaseSettings
import numpy as np


import AQiPT.AQiPTcore as aqipt

class SimulationConfig(BaseSettings):
    time_simulation: float = 5
    sampling: int = int(1e3)
    bitdepth: int = 16
    ARGS: Dict = {'sampling': sampling,
                   'bitdepth': bitdepth,
                   'time_dyn': time_simulation}
    PULSE_PARAMS: aqipt.general_params = aqipt.general_params(ARGS)  
    
    
class PulseConfig(BaseSettings):
    DEFAULT_COLORS : Dict = {'detuning' : ['firebrick','lightcoral','coral','chocolate'],
                             'coupling' : ['turquoise', 'paleturquoise','darkturquoise','skyblue'],
                             'other' : ['slateblue', 'plum','violet','mediumorchid']}
    available_pulse_shapes: List[str] = ["square", "gaussian"]


class AtomicConfig(BaseSettings):
    nr_levels: int =  4
    rydberg_states: List[int] = [2,3]
    l_values: List[int] = [1,2]
    possible_transitions: Any = "All"
    c6_constant: float = - 2*np.pi*1520
    c3_constant: float = - 2*np.pi*7950
    R: float = 2
    layout: Union[List[tuple], Any] = [(0,0,0), (0,R,0), (R,0,0), (R,R,0),(0,2*R,0)] 
    connectivity: List = ["All", []]


class TranspilerConfig(BaseSettings):
    t_start: float = 0.0
    t_wait: float = 0.01
    shape: str = "square"
    normal_frequency: float = 10.0

class BackendConfig(BaseSettings):
    simulation_config: SimulationConfig = SimulationConfig()
    pulse_config: PulseConfig = PulseConfig()
    atomic_config: AtomicConfig = AtomicConfig()
    transpiler_config: TranspilerConfig = TranspilerConfig()

    
default_backend = BackendConfig()
    