from typing import List, Dict, Tuple, Any
from pydantic_settings import BaseSettings
import numpy as np


class SimulationConfig(BaseSettings):
    """Simulation config class. 
    
    It contains the parameters used by AQiPT to build the time considerations and
    sampling of the functions involved in the simulation.

    Args:
        time_simulation (float): How long the simulation last, starting from 0
        sampling (float): How many samples are inside the simulation time
        bitdepth (int): The number of discrete levels that the function has between and the level
        nsteps (int): Number of steps for the mesolve function
        rtol (float): Error tolerance for the mesolve function
        max_steps (float): _description_ #TODO: Doc to do
        store_steps (bool): If the mesolve should save the states during the run
    """
    time_simulation: float = 5
    sampling: int = int(1e3)
    bitdepth: int = 16
    nsteps: int = 10000
    rtol: float = 1e6
    max_steps: float = 10e-6
    store_states: bool = True
    
    
class PulseConfig(BaseSettings):
    """Pulse config class.

    It contains the parameters used in the description for the pulses.
    
    Args:
        DEFAULT_COLORTS (Dict[str,List[str]]): Dictonary that contains the list of colors to use
        when plotting the pulses and results
        available_pulse_shapes (List[str]): List of the shaped pulses types inside the transpiler
    """
    DEFAULT_COLORS : Dict = {'detuning' : ['firebrick','lightcoral','coral','chocolate'],
                             'coupling' : ['turquoise', 'paleturquoise','darkturquoise','skyblue'],
                             'other' : ['slateblue', 'plum','violet','mediumorchid']}
    available_pulse_shapes: List[str] = ["square", "gaussian"]


class AtomicConfig(BaseSettings):
    """Atomic config class

    It contains all the atomic considerations inside the transpiler. This
    is the most used configuration inside the transpiler and should be taken with care.
    
    Args:
        nr_levels (int): Number of levels that each atom has (0, 1, 2, 3, ...)
        ryberg_states (List[int]): List of the states that are Rydberg states in the atom
        l_values (List[int]): List of the l quantum number for each Rydberg state
        possible_transitions: (Any): List of the possible couplings from each state to another
        c6_constant (float): Value for the Vaan der Waals interaction
        c3_constant (float): Value for the resonant interaction
        R (float): Distance between the atoms
        layout (List[Tuple[int,int,int]]): Lattice configuration of the atoms
        connectivity (List[Any]): List of the connections between states and atoms 
    """
    nr_levels: int =  4
    rydberg_states: List[int] = [2,3]
    l_values: List[int] = [1,2]
    possible_transitions: Any = "All"
    c6_constant: float = - 2*np.pi*1520
    c3_constant: float = - 2*np.pi*7950
    R: float = 2
    layout: List[Tuple[int,int,int]] = [(0,0,0), (0,R,0), (R,0,0), (R,R,0),(0,2*R,0)] 
    connectivity: List[Any] = ["All", []]


class TranspilerConfig(BaseSettings):
    """Transpiler config class

    It contains all the parameters for the transpiler to use in the process.
    
    Args:
       t_start (float): The minimum time where the pulses can start
       t_wait (float): How much time the transpiler must waits before adding another pulse
       shpae (str): The shape that most of the pulses will have
       normal_frequency (float): Frequency of coupling of most of the pulses 
    """
    t_start: float = 0.0
    t_wait: float = 0.01
    shape: str = "square"
    normal_frequency: float = 10.0

class BackendConfig(BaseSettings):
    """Backend config class

    It contains all the configuration classes for the transpiler
    
    Args:
        simulation_config (SimulationConfig): The simulation configuration for the transpiler
        pulse_config (PulseConfig): The pulse configuration for the transpiler
        atomic_config (AtomicConfig): The atomic configuration for the transpiler
        transpiler_config (TranspilerConfig): The transpiler configuration for the transpiler
    """
    simulation_config: SimulationConfig = SimulationConfig()
    pulse_config: PulseConfig = PulseConfig()
    atomic_config: AtomicConfig = AtomicConfig()
    transpiler_config: TranspilerConfig = TranspilerConfig()

# A default backend available for the whole transpiler in case none is provided   
default_backend = BackendConfig()
    