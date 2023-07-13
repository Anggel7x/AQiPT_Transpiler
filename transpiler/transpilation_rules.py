import numpy as np
from transpiler.gate_schedules.schedules import *

from transpiler.config.core import transpilation_config

freq = transpilation_config.normal_freq
shape = transpilation_config.shape
TIME_SLEEP = transpilation_config.t_wait
t_start = transpilation_config.t_start
high_freq = transpilation_config.high_freq
transpilation_rules = transpilation_config.transpilation_rules


def get_transpilation_rule(name, transpilation_rules):
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


""" (name)_rule(args):

    Transpilation rule for the (name) gate.

    Args:
        name (str): Name of the gate inside the QuantumCircuit.
        params (List[float]): List of parameters, normally angles, that some gates need.
        num_qubits (int): Number of qubits that the gate is applied
        qubits (List[int]): List that contains the number of the qubit(s) which is applied on.
        circuit_schedule (dict): Dictionary than contains the schedule of the circuit so far.

    Raises:
        ValueError: If name does not match.
        ValueError: If the number of qubits does not match.
"""


def rx_rule(name, params, num_qubits, qubits, circuit_schedule):
    
    if name != "rx":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    theta = params[0]
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max(qubit_info[1], TIME_SLEEP)
    
    # Construct the gate schedule
    Rx = RxSchedule(theta = theta, t_start=qubit_t_end, freq=freq, shape = shape)
    
    # Update the circuit schedule
    qubit_info[0].append(Rx)
    qubit_info[1] = Rx.t_end + TIME_SLEEP

def ry_rule(name, params, num_qubits, qubits, circuit_schedule):
    
    if name != "ry":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    theta = params[0]
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max(qubit_info[1], TIME_SLEEP)
    
    # Construct the gate schedule
    Ry = RySchedule(theta = theta, t_start=qubit_t_end, freq=freq, shape = shape)
    
    # Update the circuit schedule
    qubit_info[0].append(Ry)
    qubit_info[1] = Ry.t_end + TIME_SLEEP
    
def rz_rule(name, params, num_qubits, qubits, circuit_schedule):
    
    if name != "rz":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    theta = params[0]
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max(qubit_info[1], TIME_SLEEP)
    
    # Construct the gate schedule
    Rz = RzSchedule(theta = theta, t_start=qubit_t_end, freq=freq, shape = shape)
    
    # Update the circuit schedule
    qubit_info[0].append(Rz)
    qubit_info[1] = Rz.t_end + TIME_SLEEP

def x_rule(name, params, num_qubits, qubits, circuit_schedule):
    
    if name != "x":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max(qubit_info[1], TIME_SLEEP)
    
    # Construct the gate schedule
    Rx = RxSchedule(theta = np.pi, t_start=qubit_t_end, freq=freq, shape = shape)
    
    # Update the circuit schedule
    qubit_info[0].append(Rx)
    qubit_info[1] = Rx.t_end + TIME_SLEEP
    
def y_rule(name, params, num_qubits, qubits, circuit_schedule):
    
    if name != "y":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_schedule = qubit_info[0]
    qubit_t_end = max(qubit_info[1], TIME_SLEEP)
    
    # Construct the gate schedule
    Ry = RySchedule(theta = np.pi, t_start=qubit_t_end, freq=freq, shape = shape)
    
    # Update the circuit schedule
    qubit_info[0].append(Ry)
    qubit_info[1] = Ry.t_end + TIME_SLEEP
    
def z_rule(name, params, num_qubits, qubits, circuit_schedule):
    
    if name != "z":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max(qubit_info[1], TIME_SLEEP)
    
    # Construct the gate schedule
    Rz = RzSchedule(theta = np.pi, t_start=qubit_t_end, freq=freq, shape = shape)
    
    # Update the circuit schedule
    qubit_info[0].append(Rz)
    qubit_info[1] = Rz.t_end + TIME_SLEEP

def h_rule(name, params, num_qubits, qubits, circuit_schedule):
    
    if name != "h":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max(qubit_info[1], TIME_SLEEP)
    
    Uxy1 = UxySchedule(theta=np.pi/2, phi= -np.pi/2, t_start= qubit_t_end, freq=freq, shape=shape)
    Uxy2 = UxySchedule(theta=np.pi, t_start=Uxy1.t_end, freq=freq, shape=shape)

    # Update the circuit schedule
    qubit_info[0].append(Uxy1)
    qubit_info[0].append(Uxy2)
    qubit_info[1] = Uxy2.t_end + TIME_SLEEP
    
def cx_rule(name, params, num_qubits, qubits, circuit_schedule):
    
    if name != "cx":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 2:
        raise ValueError(f"Number of qubits {num_qubits} != 2")
    
    ctrl, targt = qubits[1], qubits[0]
        
    # Get the qubit list of schedules and end time
    control_info = circuit_schedule[str(ctrl)]
    control_t_end = control_info[1]
    
    # Get the qubit list of schedules and end time
    target_info = circuit_schedule[str(targt)]
    target_t_end = target_info[1] 
    
    
    t_start = max(control_t_end, target_t_end, TIME_SLEEP) # We must wait for both qubits to be relaxed
    CUxy = CUxySchedule(t_start=t_start, freq= freq, shape=shape, pair=[[1,2],[1,2]])
    
    circuit_schedule[str(ctrl)][0].append(CUxy.q_schedule[0])
    circuit_schedule[str(targt)][0].append(CUxy.q_schedule[1])

    circuit_schedule[str(ctrl)][1] = CUxy.t_end  + TIME_SLEEP
    circuit_schedule[str(targt)][1] = CUxy.t_end  + TIME_SLEEP
    
def cp_rule(name, params, num_qubits, qubits, circuit_schedule):
    
    if name != "cp":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 2:
        raise ValueError(f"Number of qubits {num_qubits} != 2")
    
    phi11 = params[0]
    c6 = - 2*np.pi*1520
    t_2 =  phi11/(np.abs(c6)/np.sqrt(2)**6)
    ctrl, targt =  qubits[0], qubits[1]
        
    # Get the qubit list of schedules and end time
    control_info = circuit_schedule[str(ctrl)]
    control_t_end = control_info[1]
    
    # Get the qubit list of schedules and end time
    target_info = circuit_schedule[str(targt)]
    target_t_end = target_info[1] 
    
    
    t_start = max(control_t_end, target_t_end, TIME_SLEEP) # We must wait for both qubits to be free
    CP = CphaseSchedule(t_start=t_start, t_2 = t_2, freq=high_freq, shape=shape)
    
    circuit_schedule[str(ctrl)][0].append(CP.q_schedule[0])
    circuit_schedule[str(targt)][0].append(CP.q_schedule[1])

    circuit_schedule[str(ctrl)][1] = CP.t_end  + TIME_SLEEP
    circuit_schedule[str(targt)][1] = CP.t_end  + TIME_SLEEP
        
def iswap_rule(name, params, num_qubits, qubits, circuit_schedule):
    
    if name != "swap" and name != "iswap":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 2:
        raise ValueError(f"Number of qubits {num_qubits} != 2")
    
    ctrl, targt =  qubits[0], qubits[1]
        
    # Get the qubit list of schedules and end time
    control_info = circuit_schedule[str(ctrl)]
    control_t_end = control_info[1] 
    
    # Get the qubit list of schedules and end time
    target_info = circuit_schedule[str(targt)]
    target_t_end = target_info[1]
    
    
    t_start = max(control_t_end, target_t_end, TIME_SLEEP) # We must wait for both qubits to be relaxed
    XY = XYSchedule(t_start=t_start, freq= freq, shape=shape)
    
    circuit_schedule[str(ctrl)][0].append(XY.q_schedule[0])
    circuit_schedule[str(targt)][0].append(XY.q_schedule[1])

    circuit_schedule[str(ctrl)][1] = XY.t_end  + TIME_SLEEP
    circuit_schedule[str(targt)][1] = XY.t_end  + TIME_SLEEP
    
transpilation_rules = {
    'rx' : rx_rule,
    'ry' : ry_rule,
    'rz' : rz_rule,
    'x' : x_rule,
    'y' : y_rule,
    'z' : z_rule,
    'h' : h_rule,
    'cx' : cx_rule,
    'cp' : cp_rule,
    'iswap' : iswap_rule,
    'swap': iswap_rule
}