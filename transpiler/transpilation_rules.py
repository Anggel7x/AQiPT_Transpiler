import numpy as np
from gate_scheduler.schedules import *

circuit_schedule = {}
freq = 1
shape = "square"
c6 = -2*np.pi*1000
TIME_SLEEP = 0


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


    if name != "rx":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    theta = params[0]
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_schedule = qubit_info[0]
    qubit_t_end = qubit_info[1]
    
    # Construct the gate schedule
    Rx = RxSchedule(theta = theta, t_start=qubit_t_end, freq=freq, shape = shape)
    
    # Update the circuit schedule
    qubit_info[0].append(Rx)
    qubit_info[1] = Rx.t_end

    
    if name != "ry":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    theta = params[0]
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_schedule = qubit_info[0]
    qubit_t_end = qubit_info[1]
    
    # Construct the gate schedule
    Ry = RySchedule(theta = theta, t_start=qubit_t_end, freq=freq, shape = shape)
    
    # Update the circuit schedule
    qubit_info[0].append(Ry)
    if name != "rz":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    theta = params[0]
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_schedule = qubit_info[0]
    qubit_t_end = qubit_info[1]
    
    # Construct the gate schedule
    Rz = RzSchedule(theta = theta, t_start=qubit_t_end, freq=freq, shape = shape)
    
    # Update the circuit schedule
    qubit_info[0].append(Rz)
    if name != "x":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_schedule = qubit_info[0]
    qubit_t_end = qubit_info[1]
    
    # Construct the gate schedule
    Rx = RxSchedule(theta = np.pi, t_start=qubit_t_end, freq=freq, shape = shape)
    
    # Update the circuit schedule
    qubit_info[0].append(Rx)
    qubit_info[1] = Rx.t_end
    
    if name != "y":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_schedule = qubit_info[0]
    qubit_t_end = qubit_info[1]
    
    # Construct the gate schedule
    Ry = RySchedule(theta = np.pi, t_start=qubit_t_end, freq=freq, shape = shape)
    
    # Update the circuit schedule
    qubit_info[0].append(Ry)
    qubit_info[1] = Ry.t_end
    
    if name != "z":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_schedule = qubit_info[0]
    qubit_t_end = qubit_info[1]
    
    # Construct the gate schedule
    Rz = RzSchedule(theta = np.pi, t_start=qubit_t_end, freq=freq, shape = shape)
    
    # Update the circuit schedule
    qubit_info[0].append(Rz)
    if name != "h":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")
    
    qubit = qubits[0]
        
    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_schedule = qubit_info[0]
    qubit_t_end = qubit_info[1]
        
    Uxy1 = UxySchedule(theta=np.pi/2, phi= -np.pi/2, t_start=qubit, freq=freq, shape=shape)
    Uxy2 = UxySchedule(theta=np.pi, t_start=Uxy1.t_end, freq=freq, shape=shape)

    # Update the circuit schedule
    qubit_info[0].append(Uxy1)
    qubit_info[0].append(Uxy2)
    qubit_info[1] = Uxy2.t_end
    
    if name != "cx":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 2:
        raise ValueError(f"Number of qubits {num_qubits} != 2")
    
    ctrl, targt = qubits[1], qubits[0]
        
    # Get the qubit list of schedules and end time
    control_info = circuit_schedule[str(ctrl)]
    control_schedule = control_info[0]
    control_t_end = control_info[1]
    
    # Get the qubit list of schedules and end time
    target_info = circuit_schedule[str(targt)]
    target_schedule = target_info[0]
    target_t_end = target_info[1]
    
    
    t_start = max(control_t_end, target_t_end) # We must wait for both qubits to be relaxed
    CUxy = CUxySchedule(t_start=t_start, freq= freq, shape=shape)
    
    circuit_schedule[str(ctrl)][0].append(CUxy.q_schedule[0])
    circuit_schedule[str(targt)][0].append(CUxy.q_schedule[1])

    if name != "cp":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 2:
        raise ValueError(f"Number of qubits {num_qubits} != 2")
    
    phi11 = params[0]
    ctrl, targt =  qubits[0], qubits[1]
        
        
    # Get the qubit list of schedules and end time
    control_info = circuit_schedule[str(ctrl)]
    control_schedule = control_info[0]
    control_t_end = control_info[1]
    
    # Get the qubit list of schedules and end time
    target_info = circuit_schedule[str(targt)]
    target_schedule = target_info[0]
    target_t_end = target_info[1]
    
    
    t_start = max(control_t_end, target_t_end) # We must wait for both qubits to be relaxed
    t2 = phi11/c6
    CP = CphaseSchedule(t_start=t_start, t_2=t2, freq= freq, shape=shape)
    
    circuit_schedule[str(ctrl)][0].append(CP.q_schedule[0])
    circuit_schedule[str(targt)][0].append(CP.q_schedule[1])

    if name != "iswap":
        raise ValueError(f"Name {name} does not match for this rule")
    
    if num_qubits != 2:
        raise ValueError(f"Number of qubits {num_qubits} != 2")
    
    ctrl, targt =  qubits[0], qubits[1]
        
    # Get the qubit list of schedules and end time
    control_info = circuit_schedule[str(ctrl)]
    control_schedule = control_info[0]
    control_t_end = control_info[1]
    
    # Get the qubit list of schedules and end time
    target_info = circuit_schedule[str(targt)]
    target_schedule = target_info[0]
    target_t_end = target_info[1]
    
    
    t_start = max(control_t_end, target_t_end) # We must wait for both qubits to be relaxed
    t2 = 3*np.pi / c6
    XY = XYSchedule(t_start=t_start, t_2 = t2, freq= freq, shape=shape)
    
    circuit_schedule[str(ctrl)][0].append(XY.q_schedule[0])
    circuit_schedule[str(targt)][0].append(XY.q_schedule[1])

    circuit_schedule[str(ctrl)][1] = XY.t_end
    circuit_schedule[str(targt)][1] = XY.t_end