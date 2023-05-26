from .transpilation_rules import *
from .rydberg_circuits import RydbergQubitSchedule, RydbergRegisterSchedule
from .gate_scheduler.UxySchedule import CERO_FUNCTION


def extract_qc_data(qc):
    gates = []

    for d in qc.data:
        name = d.operation.name
        params = d.operation.params
        num_qubits = d.operation.num_qubits
        qubits = [d.qubits[i].index for i in range(0, num_qubits)]
        gates.append((name, params, num_qubits, qubits))
        
    return gates

def circuit_schedule_init(num_qubits):
    
    """
    circuit_schedule = {
        "Qubit_#" : [ List[Schedules] , t_end ]
    }
    """
    circuit_schedule = {}

    for q in range(0, num_qubits):
        circuit_schedule[str(q)] = [[], 0]
    
    return circuit_schedule



def transpile(gates, transpilation_rules, num_qubits, **kwargs):
    circuit_schedule = circuit_schedule_init(num_qubits)
    for gate in gates:
        name, params, num_qubits, qubits = gate
        apply_rule = get_transpilation_rule(name, transpilation_rules)
        args = {
            'name' : name, 
            'params' : params, 
            'num_qubits': num_qubits, 
            'qubits' : qubits, 
            'circuit_schedule': circuit_schedule}
        apply_rule(**args)
        
    return circuit_schedule