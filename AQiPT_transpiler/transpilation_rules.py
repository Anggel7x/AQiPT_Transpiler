from typing import List, Dict, Callable
import numpy as np

from .gate_schedules.schedules import *
from .config.core import BackendConfig, default_backend


def transpilation_rule(func: Callable) -> Callable:
    """(name)_rule(args):

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

    Decorator for transpilation rules. It extracts common arguments and the backend.

    Args:
        func (_type_): _description_
    """

    def extract_backend(*args, **kwargs):
        if "backend" in kwargs.keys():
            backend_config = kwargs["backend"]
        else:
            backend_config = default_backend

        assert isinstance(backend_config, BackendConfig)

        transpiler_config = backend_config.transpiler_config
        t_wait = transpiler_config.t_wait
        freq = transpiler_config.normal_frequency
        shape = transpiler_config.shape

        atomic_config = backend_config.atomic_config
        c6 = atomic_config.c6_constant
        R = atomic_config.R

        func(t_wait=t_wait, freq=freq, shape=shape, c6=c6, R=R, *args, **kwargs)

    return extract_backend


@transpilation_rule
def uxy_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the Uxy transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "uxy"
        params (List[float]): List of parameters for the gate, theta and phi
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "uxy"
        ValueError: The number of qubits is different of 1
    """
    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "uxy":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")

    # Get the gate angles and qubit
    theta = params[0]
    phi = params[1]
    qubit = qubits[0]

    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max(qubit_info[1], t_wait)

    # Construct the gate schedule
    Uxy = UxySchedule(
        theta=theta,
        phi=phi,
        t_start=qubit_t_end,
        freq=freq,
        shape=shape,
        backend=kwargs["backend"],
    )

    # Update the circuit schedule
    qubit_info[0].append(Uxy)
    qubit_info[1] = Uxy.t_end + t_wait


@transpilation_rule
def rx_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the rx transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "rx"
        params (List[float]): List of parameters for the gate, usually angles
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "rx"
        ValueError: The number of qubits is different of 1
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "rx":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")

    theta = params[0]
    qubit = qubits[0]

    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max(qubit_info[1], t_wait)

    # Construct the gate schedule
    Rx = RxSchedule(
        theta=theta,
        t_start=qubit_t_end,
        freq=freq,
        shape=shape,
        backend=kwargs["backend"],
    )

    # Update the circuit schedule
    qubit_info[0].append(Rx)
    qubit_info[1] = Rx.t_end + t_wait


@transpilation_rule
def ry_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the ry transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "ry"
        params (List[float]): List of parameters for the gate, usually angles
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "ry"
        ValueError: The number of qubits is different of 1
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "ry":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")

    theta = params[0]
    qubit = qubits[0]

    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max(qubit_info[1], t_wait)

    # Construct the gate schedule
    Ry = RySchedule(
        theta=theta,
        t_start=qubit_t_end,
        freq=freq,
        shape=shape,
        backend=kwargs["backend"],
    )

    # Update the circuit schedule
    qubit_info[0].append(Ry)
    qubit_info[1] = Ry.t_end + t_wait


@transpilation_rule
def rz_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the rz transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "rz"
        params (List[float]): List of parameters for the gate, usually angles
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "rz"
        ValueError: The number of qubits is different of 1
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "rz":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")

    theta = params[0]
    qubit = qubits[0]

    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max(qubit_info[1], t_wait)

    # Construct the gate schedule
    Rz = RzSchedule(
        theta=theta,
        t_start=qubit_t_end,
        freq=freq,
        shape=shape,
        backend=kwargs["backend"],
    )

    # Update the circuit schedule
    qubit_info[0].append(Rz)
    qubit_info[1] = Rz.t_end + t_wait


@transpilation_rule
def x_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the x transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "x"
        params (List[float]): List of parameters for the gate, usually angles
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "x"
        ValueError: The number of qubits is different of 1
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "x":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")

    qubit = qubits[0]

    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max(qubit_info[1], t_wait)

    # Construct the gate schedule
    Rx = RxSchedule(
        theta=np.pi,
        t_start=qubit_t_end,
        freq=freq,
        shape=shape,
        backend=kwargs["backend"],
    )

    # Update the circuit schedule
    qubit_info[0].append(Rx)
    qubit_info[1] = Rx.t_end + t_wait


@transpilation_rule
def y_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the y transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "y"
        params (List[float]): List of parameters for the gate, usually angles
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "y"
        ValueError: The number of qubits is different of 1
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "y":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")

    qubit = qubits[0]

    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_schedule = qubit_info[0]
    qubit_t_end = max(qubit_info[1], t_wait)

    # Construct the gate schedule
    Ry = RySchedule(
        theta=np.pi,
        t_start=qubit_t_end,
        freq=freq,
        shape=shape,
        backend=kwargs["backend"],
    )

    # Update the circuit schedule
    qubit_info[0].append(Ry)
    qubit_info[1] = Ry.t_end + t_wait


@transpilation_rule
def z_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the z transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "z"
        params (List[float]): List of parameters for the gate, usually angles
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "z"
        ValueError: The number of qubits is different of 1
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "z":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")

    qubit = qubits[0]

    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max(qubit_info[1])

    # Construct the gate schedule
    Rz = RzSchedule(
        theta=np.pi,
        t_start=qubit_t_end,
        freq=freq,
        shape=shape,
        backend=kwargs["backend"],
    )

    # Update the circuit schedule
    qubit_info[0].append(Rz)
    qubit_info[1] = Rz.t_end + t_wait


@transpilation_rule
def h_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the h transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "h"
        params (List[float]): List of parameters for the gate, usually angles
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "h"
        ValueError: The number of qubits is different of 1
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "h":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 1:
        raise ValueError(f"Number of qubits {num_qubits} != 1")

    qubit = qubits[0]

    # Get the qubit list of schedules and end time
    qubit_info = circuit_schedule[str(qubit)]
    qubit_t_end = max([qubit_info[1] for qubit_info in circuit_schedule.values()])

    Uxy1 = UxySchedule(
        theta=np.pi / 2,
        phi=-np.pi / 2,
        t_start=qubit_t_end,
        freq=freq,
        shape=shape,
        backend=kwargs["backend"],
    )
    Uxy2 = UxySchedule(
        theta=np.pi,
        t_start=Uxy1.t_end,
        freq=freq,
        shape=shape,
        backend=kwargs["backend"],
    )

    # Update the circuit schedule
    qubit_info[0].append(Uxy1)
    qubit_info[0].append(Uxy2)
    qubit_info[1] = Uxy2.t_end + t_wait


@transpilation_rule
def cuxy_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the cuxy transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "cuxy"
        params (List[float]): List of parameters for the gate, theta and phi
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "cuxy"
        ValueError: The number of qubits is different of 2
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "cuxy":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 2:
        raise ValueError(f"Number of qubits {num_qubits} != 2")

    theta = params[0]
    phi = params[1]
    ctrl, targt = qubits[0], qubits[1]

    # Get the qubit list of schedules and end time
    control_info = circuit_schedule[str(ctrl)]
    control_t_end = control_info[1]

    # Get the qubit list of schedules and end time
    target_info = circuit_schedule[str(targt)]
    target_t_end = target_info[1]

    t_start = max(
        control_t_end, target_t_end, t_wait
    )  # We must wait for both qubits to be free
    CUxy = CUxySchedule(
        t_start=t_start,
        theta=theta,
        phi=phi,
        freq=freq,
        shape=shape,
        backend=kwargs["backend"],
    )

    circuit_schedule[str(ctrl)][0].append(CUxy.q_schedule[0])
    circuit_schedule[str(targt)][0].append(CUxy.q_schedule[1])

    circuit_schedule[str(ctrl)][1] = CUxy.t_end + t_wait
    circuit_schedule[str(targt)][1] = CUxy.t_end + t_wait


@transpilation_rule
def cx_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the cx transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "cx"
        params (List[float]): List of parameters for the gate
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "cx"
        ValueError: The number of qubits is different of 2
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "cx":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 2:
        raise ValueError(f"Number of qubits {num_qubits} != 2")

    theta = np.pi
    phi = 0
    ctrl, targt = qubits[0], qubits[1]

    # Get the qubit list of schedules and end time
    control_info = circuit_schedule[str(ctrl)]
    control_t_end = control_info[1]

    # Get the qubit list of schedules and end time
    target_info = circuit_schedule[str(targt)]
    target_t_end = target_info[1]

    t_start = max(
        control_t_end, target_t_end, t_wait
    )  # We must wait for both qubits to be free
    CUxy = CUxySchedule(
        t_start=t_start,
        theta=theta,
        phi=phi,
        freq=freq,
        shape=shape,
        backend=kwargs["backend"],
    )

    circuit_schedule[str(ctrl)][0].append(CUxy.q_schedule[0])
    circuit_schedule[str(targt)][0].append(CUxy.q_schedule[1])

    circuit_schedule[str(ctrl)][1] = CUxy.t_end + t_wait
    circuit_schedule[str(targt)][1] = CUxy.t_end + t_wait


@transpilation_rule
def cp_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the cp transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "cp"
        params (List[float]): List of parameters for the gate, phi_11
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "cp"
        ValueError: The number of qubits is different of 2
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "cp":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 2:
        raise ValueError(f"Number of qubits {num_qubits} != 2")

    phi11 = params[0]
    ctrl, targt = qubits[0], qubits[1]

    # Get the qubit list of schedules and end time
    control_info = circuit_schedule[str(ctrl)]
    control_t_end = control_info[1]

    # Get the qubit list of schedules and end time
    target_info = circuit_schedule[str(targt)]
    target_t_end = target_info[1]

    t_start = max(
        [qubit_info[1] for qubit_info in circuit_schedule.values()]
    )  # We must wait for both qubits to be free
    CP = CphaseSchedule(
        t_start=t_start, phi11=phi11, freq=freq, shape=shape, backend=kwargs["backend"]
    )

    circuit_schedule[str(ctrl)][0].append(CP.q_schedule[0])
    circuit_schedule[str(targt)][0].append(CP.q_schedule[1])

    circuit_schedule[str(ctrl)][1] = CP.t_end + t_wait
    circuit_schedule[str(targt)][1] = CP.t_end + t_wait


@transpilation_rule
def cz_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the cp transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "cp"
        params (List[float]): List of parameters for the gate, phi_11
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "cp"
        ValueError: The number of qubits is different of 2
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "cp" or name != "":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 2:
        raise ValueError(f"Number of qubits {num_qubits} != 2")

    phi11 = np.pi
    ctrl, targt = qubits[0], qubits[1]

    # Get the qubit list of schedules and end time
    control_info = circuit_schedule[str(ctrl)]
    control_t_end = control_info[1]

    # Get the qubit list of schedules and end time
    target_info = circuit_schedule[str(targt)]
    target_t_end = target_info[1]

    t_start = max(
        [qubit_info[1] for qubit_info in circuit_schedule.values()]
    )  # We must wait for both qubits to be free
    CP = CphaseSchedule(
        t_start=t_start, phi11=phi11, freq=freq, shape=shape, backend=kwargs["backend"]
    )

    print(kwargs["backend"])

    circuit_schedule[str(ctrl)][0].append(CP.q_schedule[0])
    circuit_schedule[str(targt)][0].append(CP.q_schedule[1])

    circuit_schedule[str(ctrl)][1] = CP.t_end + t_wait
    circuit_schedule[str(targt)][1] = CP.t_end + t_wait


@transpilation_rule
def iswap_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the iswap transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "iswap"
        params (List[float]): List of parameters for the gate, theta and phi
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "iswap"
        ValueError: The number of qubits is different of 2
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "swap" and name != "iswap":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 2:
        raise ValueError(f"Number of qubits {num_qubits} != 2")

    ctrl, targt = qubits[0], qubits[1]

    # Get the qubit list of schedules and end time
    control_info = circuit_schedule[str(ctrl)]
    control_t_end = control_info[1]

    # Get the qubit list of schedules and end time
    target_info = circuit_schedule[str(targt)]
    target_t_end = target_info[1]

    t_start = max(
        [qubit_info[1] for qubit_info in circuit_schedule.values()]
    )  # We must wait for both qubits to be relaxed
    XY = XYSchedule(t_start=t_start, freq=freq, shape=shape, backend=kwargs["backend"])

    circuit_schedule[str(ctrl)][0].append(XY.q_schedule[0])
    circuit_schedule[str(targt)][0].append(XY.q_schedule[1])

    circuit_schedule[str(ctrl)][1] = XY.t_end + t_wait
    circuit_schedule[str(targt)][1] = XY.t_end + t_wait


@transpilation_rule
def xy_rule(
    name: str,
    params: List[float],
    num_qubits: int,
    qubits: List[int],
    circuit_schedule: Dict[str, List],
    **kwargs,
):
    """The application for the xy transpilation rule.

    Args:
        name (str): Name of the gate received. Must be equalt to "xy"
        params (List[float]): List of parameters for the gate, Theta
        num_qubits (int): Number of qubits where the gate is applied
        qubits (List[int]): List of integer index for the qubits
        circuit_schedule (Dict[str, List]): Dictionary containing the prototype of the circuit schedule.

    Raises:
        ValueError: The name does not match "xy"
        ValueError: The number of qubits is different of 2
    """

    t_wait = kwargs["t_wait"]
    freq = kwargs["freq"]
    shape = kwargs["shape"]

    if name != "xy":
        raise ValueError(f"Name {name} does not match for this rule")

    if num_qubits != 2:
        raise ValueError(f"Number of qubits {num_qubits} != 2")

    ctrl, targt = qubits[0], qubits[1]

    # Get the qubit list of schedules and end time
    control_info = circuit_schedule[str(ctrl)]
    control_t_end = control_info[1]

    # Get the qubit list of schedules and end time
    target_info = circuit_schedule[str(targt)]
    target_t_end = target_info[1]

    theta = params[0]

    t_start = max(
        control_t_end, target_t_end, t_wait
    )  # We must wait for both qubits to be relaxed
    XY = XYSchedule(
        theta=theta, t_start=t_start, freq=freq, shape=shape, backend=kwargs["backend"]
    )

    circuit_schedule[str(ctrl)][0].append(XY.q_schedule[0])
    circuit_schedule[str(targt)][0].append(XY.q_schedule[1])

    circuit_schedule[str(ctrl)][1] = XY.t_end + t_wait
    circuit_schedule[str(targt)][1] = XY.t_end + t_wait


transpilation_rules = {
    # One qubit rules
    "uxy": uxy_rule,
    "rx": rx_rule,
    "ry": ry_rule,
    "rz": rz_rule,
    "x": x_rule,
    "y": y_rule,
    "z": z_rule,
    "h": h_rule,
    # Two qubit rules
    "cuxy": cuxy_rule,
    "cx": cx_rule,
    "cp": cp_rule,
    "xy": xy_rule,
    "iswap": iswap_rule,
    "swap": iswap_rule,
    "cz": cz_rule,
}
