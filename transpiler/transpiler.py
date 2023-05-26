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

        print(f"{name}, {params}, {num_qubits}, {qubits}")
        gates.append((name, params, num_qubits, qubits))
        
    return gates

def def_tstart(qubit_schedule):
    
    t_start = qubit_schedule[1]
    return t_start + TIME_SLEEP

def circuit_schedule_init():
    circuit_schedule = {}

    for q in range(0, qc.qregs[0].size):
        circuit_schedule[str(q)] = [[], 0]
    
    return circuit_schedule

def transpile(gates):
    for gate in gates:
        name, params, num_qubits, qubits = gate
        apply_rule = get_transpilation_rule(name)
        args = {'name' : name, 'params' : params, 'num_qubits': num_qubits, 'qubits' : qubits}
        apply_rule(**args)
        
    return circuit_schedule