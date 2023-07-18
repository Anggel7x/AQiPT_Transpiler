from typing import Dict, Optional
from qiskit import QuantumCircuit
import time
from transpiler.config.core import BackendConfig, backend
from transpiler.rydberg_blocks.rydberg_qubits import *
from transpiler.utils.transpiler_utils import *
from transpiler.transpilation_rules import transpilation_rules

class Transpiler():
    
    def __init__(self,
                 qc: QuantumCircuit,
                 backend_config: Optional[BackendConfig] = backend,
                 transpilation_rules: Optional[Dict] = transpilation_rules,
                 *args, **kwargs) -> None:
        
        self.qc = qc
        self.backend_config = backend_config
        self.transpilation_rules = transpilation_rules
        
    def transpile(self) -> RydbergRegisterSchedule:
        
        time_start = time.time()
        
        rydberg_schedule = qc_to_ryd(self.qc, self.transpilation_rules, backend=self.backend_config)
        self.rydberg_schedule = rydberg_schedule
        time_end = time.time()
        self.transpilation_time = time_end - time_start
        self.rydberg_schedule = rydberg_schedule
        return rydberg_schedule
    
    def build_transpiled_circuit(self, init_state)-> RydbergQuantumRegister:
        
        schedules = self.rydberg_schedule.schedules
        atomic_config = self.backend_config.atomic_config
        qubits = []
        for i, sch in enumerate(schedules):
            qubit = RydbergQubit(
                nr_levels = atomic_config.nr_levels,
                name = f"Qubit {i}",
                initial_state=0,
                schedule=sch,
                rydberg_states= {
                    'RydbergStates' : atomic_config.rydberg_states,
                    "l_value": atomic_config.l_values
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
        
        qr.compile()
        
        self.quantum_register = qr
        
        return qr
        
        
        