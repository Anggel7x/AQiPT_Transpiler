from typing import Callable
from transpiler.transpilation_rules import *
from transpiler.rydberg_blocks.rydberg_qubits import RydbergQubitSchedule, RydbergRegisterSchedule
from transpiler.gate_schedules.UxySchedule import CERO_FUNCTION
from transpiler.utils.transpiler_utils import *

def get_transpilation_rule(name, transpilation_rules) -> Callable:
    """This function gets the functional asociation between the name
    of the gate and the defined transpilation rules.

    Args:
        name (str): Name of the gate inside the QuantumCircuit.
        transpilation_rules (dic): Defined transpilation rules.

    Raises:
        ValueError: If there's no rule defined for the name of the gate.

    Returns:
        func: Function that describes the transpilation rule.
    """
    try:
        return transpilation_rules[name]
    except:
        raise ValueError(f'No transpilation rule for {name}')

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
        if name == "barrier": continue 
        apply_rule = get_transpilation_rule(name, transpilation_rules)
        args = {
            'name' : name, 
            'params' : params, 
            'num_qubits': num_qubits, 
            'qubits' : qubits, 
            'circuit_schedule': circuit_schedule}
        apply_rule(**args, **kwargs)
        
    return circuit_schedule


def construct_register_schedule(circuit_schedule, num_qubits, **kwargs):
    register_schedule = []
    for i in range(0, num_qubits):
        
        # get the list of schedules of the qubit

        qubit_schedules = circuit_schedule[str(i)][0]
        qubit_couplings = {}
        qubit_detunings = {}
        if qubit_schedules != []:
            
            q_couplings = [ q_s.q_schedule.coupling_pulses for q_s in qubit_schedules]
        
            for j, q_c in enumerate(q_couplings):
                for i, value in enumerate(q_c.values()):
                    pair = value[0]
                    freq = value[1]
                    func = value[2]
                    qubit_couplings[f'Coupling{i+j}'] = [pair, freq, func]
        
            q_detunings = [ q_s.q_schedule.detuning_pulses for q_s in qubit_schedules]
            
            for j, q_c in enumerate(q_detunings):
                for i, value in enumerate(q_c.values()):
                    pair = value[0]
                    freq = value[1]
                    func = value[2]
                                
                    qubit_detunings[f'Detuning{i+j}'] = [pair, freq, func]
            
            # Construct qubit schedule
            qubit_schedule = RydbergQubitSchedule(coupling_pulses=qubit_couplings, detuning_pulses=qubit_detunings, **kwargs)
        else:
            qubit_couplings = {'Coupling0' : [[0,1], 0, CERO_FUNCTION.function]}
            qubit_schedule = RydbergQubitSchedule(coupling_pulses=qubit_couplings, detuning_pulses=qubit_couplings, **kwargs)
            
        register_schedule.append(qubit_schedule)
    
    return register_schedule


def qc_to_ryd(qc, transpilation_rules, backend: BackendConfig = default_backend):
    gates = extract_qc_data(qc)
    num_qubits = qc.qregs[0].size
    circuit_schedule = {}
    circuit_schedule = transpile(gates, transpilation_rules, num_qubits, backend=backend)
    register_sch = construct_register_schedule(circuit_schedule, num_qubits, backend=backend)
    return RydbergRegisterSchedule(register_sch)
    
    
