from typing import List, Tuple, Callable
from AQiPT_transpiler.utils.rydberg_circuit import RydbergQuantumCircuit
from AQiPT_transpiler.transpilation_rules import (
    transpilation_rules as default_transp_rules,
)
from AQiPT_transpiler.rydberg_blocks.rydberg_schedules import (
    RydbergQubitSchedule,
    RydbergRegisterSchedule,
)
from AQiPT_transpiler.gate_schedules.uxy_schedule import CERO_FUNCTION
from AQiPT_transpiler.config.core import BackendConfig, default_backend


def get_transpilation_rule(name: str, transpilation_rules: dict) -> Callable:
    r"""Función que retorna la regla de transpilación asociada al nombre
    de una compuerta.

    Args:
        name (str): Nombre de la compuerta.
        transpilation_rules (dict): Reglas de transpilación disponibles.

    Raises:
        ValueError: Si la regla de transpilación para el nombre no existe.

    Returns:
        Callable: Regla de transpilación asociada al nombre.
    """
    try:
        return transpilation_rules[name]
    except Exception as exc:
        raise ValueError(f"No transpilation rule for {name}") from exc


def extract_qc_data(
    qc: RydbergQuantumCircuit,
) -> List[Tuple[str, List[float], int, List[int]]]:
    r"""Extrae los datos de un RydbergQuantumCircuit y los retorna
    en una lista que contiene el nombre, lista de parametros, numero de qubits
    y lista de los indices de qubits.

    Args:
        qc (RydbergQuantumCircuit): Circuito donde se sacarán los datos

    Returns:
        List[Tuple[str, List[float], int, List[int]]]: Lista de datos
    """
    gates = []

    for d in qc.data:
        name = d.operation.name
        params = d.operation.params
        num_qubits = d.operation.num_qubits
        qubits = [d.qubits[i].index for i in range(0, num_qubits)]
        gates.append((name, params, num_qubits, qubits))

    return gates


def circuit_schedule_init(num_qubits: int) -> dict:
    r"""Inicializa la estructura auxiliar del circuit schedule

    circuit_schedule = {
        "Qubit_#" : [ List[Schedules] , t_end ]
    }

    Args:
        num_qubits (int): Número de qubits del circuito.

    Returns:
        dict: La estructura auxiliar vacia construidoa.
    """
    circuit_schedule = {}

    for q in range(0, num_qubits):
        circuit_schedule[str(q)] = [[], 0]

    return circuit_schedule


def transpile_circ_sch(
    gates: list, transpilation_rules: dict, num_qubits: int, **kwargs
) -> dict:
    r"""Transpila el circuito sobre un circuit_schedule.

    Args:
        gates (list): Lista de los datos del circuito.
        transpilation_rules (dict): Reglas de transpilación disponibles.
        num_qubits (int): Número de qubits.

    Returns:
        dict: circuit_schedule con todo el circuito transpilado.
    """
    circuit_schedule = circuit_schedule_init(num_qubits)
    for gate in gates:
        name, params, num_qubits, qubits = gate
        if name == "barrier":
            continue
        apply_rule = get_transpilation_rule(name, transpilation_rules)
        args = {
            "name": name,
            "params": params,
            "num_qubits": num_qubits,
            "qubits": qubits,
            "circuit_schedule": circuit_schedule,
        }
        apply_rule(**args, **kwargs)

    return circuit_schedule


def construct_register_schedule(
    circuit_schedule: dict, num_qubits: int, **kwargs
) -> RydbergRegisterSchedule:
    r"""Función que convierte un circuit_schedule en un RydbergRegisterSchedule

    Args:
        circuit_schedule (dict): circuit_schedule que contienen el circuito
        transpilado.
        num_qubits (int): Número de qubits del circuito.

    Returns:
        RydbergRegisterSchedule: Contiene todo el schedule del circuito.
    """
    register_schedule = []
    for i in range(0, num_qubits):
        # get the list of schedules of the qubit

        qubit_schedules = circuit_schedule[str(i)][0]
        qubit_couplings = {}
        qubit_detunings = {}
        if qubit_schedules != []:
            q_couplings = [q_s.q_schedule.coupling_pulses for q_s in qubit_schedules]

            for j, q_c in enumerate(q_couplings):
                for i, value in enumerate(q_c.values()):
                    pair = value[0]
                    freq = value[1]
                    func = value[2]
                    qubit_couplings[f"Coupling{i+j}"] = [pair, freq, func]

            q_detunings = [q_s.q_schedule.detuning_pulses for q_s in qubit_schedules]

            for j, q_c in enumerate(q_detunings):
                for i, value in enumerate(q_c.values()):
                    pair = value[0]
                    freq = value[1]
                    func = value[2]

                    qubit_detunings[f"Detuning{i+j}"] = [pair, freq, func]

            # Construct qubit schedule
            qubit_schedule = RydbergQubitSchedule(
                coupling_pulses=qubit_couplings,
                detuning_pulses=qubit_detunings,
                **kwargs,
            )
        else:
            qubit_couplings = {
                "Coupling0": [
                    [0, 1],
                    0,
                    CERO_FUNCTION(backend=kwargs["backend"]).function,
                ]
            }
            qubit_schedule = RydbergQubitSchedule(
                coupling_pulses=qubit_couplings,
                detuning_pulses=qubit_couplings,
                **kwargs,
            )

        register_schedule.append(qubit_schedule)

    return RydbergRegisterSchedule(register_schedule, **kwargs)


def qc_to_ryd(
    qc: RydbergQuantumCircuit,
    transpilation_rules: dict = default_transp_rules,
    backend: BackendConfig = default_backend,
) -> RydbergRegisterSchedule:
    r"""Transpila un RydbergQuantumCircuit y lo devuelve en su forma
    RydbergRegisterSchedule.

    Args:
        qc (RydbergQuantumCircuit): Circuito a transpilar.
        transpilation_rules (dict, optional): Reglas de transpilación a utilizar. Defaults to default_transp_rules.
        backend (BackendConfig, optional): Configuración del backend a utilizar. Defaults to default_backend.

    Returns:
        RydbergRegisterSchedule: Schedule del circuito transpilado.
    """
    gates = extract_qc_data(qc)
    num_qubits = qc.qregs[0].size
    circuit_schedule = {}
    circuit_schedule = transpile_circ_sch(
        gates, transpilation_rules, num_qubits, backend=backend
    )
    register_sch = construct_register_schedule(
        circuit_schedule, num_qubits, backend=backend
    )
    return register_sch
