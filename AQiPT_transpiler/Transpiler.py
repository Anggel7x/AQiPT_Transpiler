import time
from typing import Any, Dict, Optional, Union
from .config.core import BackendConfig, default_backend
from .rydberg_blocks.rydberg_qubits import *
from .utils.transpiler_utils import *
from .transpilation_rules import transpilation_rules

class Transpiler():
    
    
    def __init__(self,
                 backend_config: Optional[BackendConfig] = default_backend,
                 transpilation_rules: Optional[Dict] = transpilation_rules,
                 *args: Any, **kwargs: Any) -> None:
        
       
        self.backend_config = backend_config
        self.transpilation_rules = transpilation_rules
        
        
    def transpile(self, qc) -> RydbergRegisterSchedule:
        
        self.qc = qc
        time_start = time.time()
        rydberg_schedule = qc_to_ryd(qc, self.transpilation_rules, backend=self.backend_config)
        self.rydberg_schedule = rydberg_schedule
        time_end = time.time()
        
        self.transpilation_time = time_end - time_start
        self.rydberg_schedule = rydberg_schedule
        return rydberg_schedule
    
    def build_transpiled_circuit(self, init_state)-> Union[RydbergQuantumRegister, RydbergQubit]:
        
        schedules = self.rydberg_schedule.schedules
        atomic_config = self.backend_config.atomic_config
        qubits = []
        
        if len(schedules) == 1:
            qubit = RydbergQubit(
                nr_levels = atomic_config.nr_levels,
                name = f"Qubit 0",
                initial_state=init_state,
                schedule=schedules[0],
                rydberg_states= {
                    'RydbergStates' : atomic_config.rydberg_states,
                    "l_values": atomic_config.l_values
                },
                backend = self.backend_config
            )
            
            self.quantum_register = qubit
            qubit.build()
            return qubit
        
        for i, sch in enumerate(schedules):
            qubit = RydbergQubit(
                nr_levels = atomic_config.nr_levels,
                name = f"Qubit {i}",
                initial_state= 0,
                schedule=sch,
                rydberg_states= {
                    'RydbergStates' : atomic_config.rydberg_states,
                    "l_values": atomic_config.l_values
                },
                backend = self.backend_config
            )
            
            qubit.compile()
            qubits.append(qubit)
            
        qr = RydbergQuantumRegister(
            qubits = qubits,
            layout = atomic_config.layout[:len(qubits)],
            init_state=init_state,
            connectivity=atomic_config.connectivity,
            c3 = atomic_config.c3_constant,
            c6 = atomic_config.c6_constant,
            backend = self.backend_config
        )
        
        qr.build()
        
        self.quantum_register = qr
        
        return qr
    
    def __call__(self) -> Any:
        return self.transpile()
     
default_transpiler =  Transpiler()