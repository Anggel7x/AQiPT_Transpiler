import numpy as np
from qiskit import *
from qiskit.circuit import Gate
from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator
from qiskit.circuit.parameterexpression import ParameterValueType
from typing import List, Optional, Union
from qiskit.circuit.library.standard_gates.u3 import U3Gate, CU3Gate


class RydbergUxyGate(Gate):
    """
    Clase que contine la transformación Uxy(theta, phi) en átomos de Rydberg.
    Hereda todas las cualidades de la clase Gate de Qiskit
    """

    def __init__(
        self,
        theta: ParameterValueType,
        phi: ParameterValueType,
        label: Optional[str] = None,
    ):
        super().__init__("uxy", 1, [theta, phi], label=label)

    def _define(self):
        """
        Definición circuital de la transformación a base de U3Gate()
        """
        qc = RydbergQuantumCircuit(1, name=self.name)

        t = self.params[0]
        p = -(np.pi / 2 + self.params[1])
        l = -p

        qc.append(U3Gate(t, p, l), [0], [])
        self.definition = qc

    def __array__(self, dtype=complex) -> np.array:
        """
        Definición matricial de la transformación como un numpy.array
        """
        theta, phi = self.params
        theta, phi = float(theta), float(phi)

        cos = np.cos(theta / 2)
        sin = np.sin(theta / 2)
        epp = np.exp(1j * phi)
        epm = np.exp(1j * (-phi))

        return (
            1
            / np.sqrt(2)
            * -1j
            * np.array([[cos, -1j * sin * epp], [-1j * sin * epm, cos]], dtype=dtype)
        )


class RydbergHGate(Gate):
    """
    Clase que contiene la transformación de Hadamard en átomos de Rydberg.
    Hereda todas las cualidades de la clase Gate de Qiskit
    """

    def __init__(self, label: Optional[str] = None):
        super().__init__("h", 1, [], label=label)

    def _define(self):
        """
        Definición circuital de la transformación a base de Uxy() de Rydberg
        """
        qc = RydbergQuantumCircuit(1, name=self.name)
        qc.append(RydbergUxyGate(np.pi / 2, -np.pi / 2), [0])
        qc.append(RydbergUxyGate(np.pi, 0), [0])
        self.definition = qc

    def __array__(self, dtype=complex) -> np.array:
        """
        Definición matricial de la transformación como un numpy.array
        """

        return 1 / np.sqrt(2) * -1j * np.array([[-1, 1], [1, 1]], dtype=dtype)


class RydbergRxGate(Gate):
    """
    Clase que contiene la transformación de Rx(theta) en átomos de Rydberg.
    Hereda todas las cualidades de la clase Gate de Qiskit
    """

    def __init__(self, theta: ParameterValueType, label: Optional[str] = None):
        super().__init__("rx", 1, [theta], label=label)

    def _define(self):
        """
        Definición circuital de la transformación a base de Uxy() de Rydberg
        """
        qc = RydbergQuantumCircuit(1, name=self.name)
        qc.append(RydbergUxyGate(self.params[0], 0), [0])
        self.definition = qc


class RydbergRyGate(Gate):
    """
    Clase que contiene la transformación de Ry(theta) en átomos de Rydberg.
    Hereda todas las cualidades de la clase Gate de Qiskit
    """

    def __init__(self, theta: ParameterValueType, label: Optional[str] = None):
        super().__init__("ry", 1, [theta], label=label)

    def _define(self):
        """
        Definición circuital de la transformación a base de Uxy() de Rydberg
        """
        qc = RydbergQuantumCircuit(1, name=self.name)
        qc.append(RydbergUxyGate(self.params[0], -np.pi / 2), [0])
        self.definition = qc


class RydbergRzGate(Gate):
    """
    Clase que contiene la transformación de Rz(theta) en átomos de Rydberg.
    Hereda todas las cualidades de la clase Gate de Qiskit
    """

    def __init__(self, theta: ParameterValueType, label: Optional[str] = None):
        super().__init__("rz", 1, [theta], label=label)

    def _define(self):
        """
        Definición circuital de la transformación a base de Uxy() de Rydberg
        """
        qc = RydbergQuantumCircuit(1, name=self.name)
        qc.append(RydbergUxyGate(np.pi / 2, -np.pi / 2), [0])
        qc.append(RydbergUxyGate(self.params[0], 0), [0])
        qc.append(RydbergUxyGate(np.pi / 2, np.pi / 2), [0])
        self.definition = qc


class RydbergCUxyGate(Gate):
    """
    Clase que contiene la transformación de Control-Uxy(theta, phi) en átomos de Rydberg.
    Hereda todas las cualidades de la clase Gate de Qiskit
    """

    def __init__(
        self,
        theta: ParameterValueType,
        phi: ParameterValueType,
        label: Optional[str] = None,
    ):
        super().__init__("cuxy", 2, [theta, phi], label=label)

    def _define(self):
        """
        Definición circuital de la transformación a base de CU3Gate() de Qiskit
        """
        qc = RydbergQuantumCircuit(2, name=self.name)

        t = self.params[0]
        p = -(np.pi / 2 + self.params[1])
        l = -p

        qc.append(CU3Gate(t, p, l), [0, 1], [])
        self.definition = qc

    def __array__(self, dtype=complex):
        """
        Definición matricial de la transformación como un numpy.array
        """
        theta, phi = self.params
        theta, phi = float(theta), float(phi)

        cos = np.cos(theta / 2)
        sin = np.sin(theta / 2)
        epp = np.exp(1j * phi)
        epm = np.exp(1j * (-phi))

        return np.array(
            [
                [cos, -1j * sin * epp, 0, 0],
                [-1j * sin * epm, cos, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ],
            dtype=dtype,
        )


class RydbergCPhase(Gate):
    """
    Clase que contiene la transformación de CPhase(phi00, phi01, phi10, phi11) en átomos de Rydberg.
    Hereda todas las cualidades de la clase Gate de Qiskit.
    """

    def __init__(
        self,
        phi11: ParameterValueType,
        label: Optional[str] = None,
    ):
        super().__init__("cp", 2, [phi11], label=label)

    def _define(self):
        """
        Definición circuital de la transformación a base de un operador matricial.
        """
        phi11 = self.params
        e00 = np.exp(1j * 0)
        e01 = np.exp(1j * np.pi)
        e10 = np.exp(1j * np.pi)
        e11 = np.exp(1j * phi11)

        qc = RydbergQuantumCircuit(2, name=self.name)

        cp = Operator(
            np.array(
                [
                    [e00, 0, 0, 0],
                    [0, e01, 0, 0],
                    [0, 0, e10, 0],
                    [0, 0, 0, e11],
                ]
            )
        )
        qc.unitary(cp, [0, 1])
        self.definition = qc

    def __array__(self, dtype=complex):
        """
        Definición matricial de la transformación como un numpy.array
        """
        phi11 = self.params

        e00 = np.exp(1j * 0)
        e01 = np.exp(1j * np.pi)
        e10 = np.exp(1j * np.pi)
        e11 = np.exp(1j * phi11)

        return np.array(
            [
                [e00, 0, 0, 0],
                [0, e01, 0, 0],
                [0, 0, e10, 0],
                [0, 0, 0, e11],
            ],
            dtype=dtype,
        )


class RydbergCXGate(Gate):
    """
    Clase que contiene la transformación Control-X en átomos de Rydberg.
    """

    def __init__(
        self,
        label: Optional[str] = None,
    ):
        super().__init__("cx", 2, [], label=label)

    def _define(self):
        """
        Definición de la transformación a base de un operador matricial
        """
        phi = self.params
        ep = 1 * np.exp(1j * phi)

        qc = RydbergQuantumCircuit(2, name=self.name)

        cp = Operator(
            np.array(
                [
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, ep],
                ]
            )
        )
        qc.unitary(cp, [0, 1])
        self.definition = qc


class RydbergXYGate(Gate):
    """
    Clase que contiene la transformación Swap en átomos de Rydberg
    """

    def __init__(
        self,
        theta: ParameterValueType,
        label: Optional[str] = None,
    ):
        super().__init__("xy", 2, [theta], label=label)

    def _define(self):
        """
        Definición circuital de la transformación a base de un operador matricial.
        """
        theta = self.params

        qc = RydbergQuantumCircuit(2, name=self.name)

        xy = Operator(
            np.array(
                [
                    [1, 0, 0, 0],
                    [0, np.cos(theta / 2), -1j * np.sin(theta / 2), 0],
                    [0, -1j * np.sin(theta / 2), np.cos(theta / 2), 0],
                    [0, 0, 0, 1],
                ]
            )
        )
        qc.unitary(xy, [0, 1])
        self.definition = qc

    def __array__(self, dtype=complex):
        """
        Definición matricial de la transformación como un numpy.array
        """
        theta = self.params

        return np.array(
            [
                [1, 0, 0, 0],
                [0, np.cos(theta / 2), -1j * np.sin(theta / 2), 0],
                [0, -1j * np.sin(theta / 2), np.cos(theta / 2), 0],
                [0, 0, 0, 1],
            ],
            dtype=dtype,
        )


class RydbergSwapGate(Gate):
    """
    Clase que contiene la transformación Swap en átomos de Rydberg
    """

    def __init__(
        self,
        label: Optional[str] = None,
    ):
        super().__init__("swap", 2, [], label=label)

    def _define(self):
        """
        Definición circuital a base de un operador matricial
        """
        qc = RydbergQuantumCircuit(2, name=self.name)

        cp = Operator(
            np.array(
                [
                    [1, 0, 0, 0],
                    [0, 0, 1j, 0],
                    [0, 1j, 0, 0],
                    [0, 0, 0, 1],
                ]
            )
        )
        qc.unitary(cp, [0, 1])
        self.definition = qc

        self.define = qc


class RydbergQuantumCircuit(QuantumCircuit):
    """
    Clase que contiene todas las transformaciones posibles en átomos de Rydberg.
    Hereda todas las funciones de QuantumCircuit de Qiksit.

    Args:
        regs (QuantumRegister y/o ClassicalRegister): Registros cuánticos y/o clásicos
        predefinidos. También puede tomar valores enteros para crear los registros de acuerdo
        al tamaño del entero.

    Returns:
        QuantumCircuit: Modelo de circuito cuántico con las transformaciones sobre átomos
        de Rydberg.
    """

    """Native Rydberg Quantum Gates"""

    def uxy(self, theta: float, phi: float, qubit: Union[int, List[int]]):
        """
        Método que aplica la transformación Uxy(theta, phi) sobre 'qubit'.

        Args:
            theta (float): Ángulo de rotación theta
            phi (float): Ángulo de rotación phi
            qubit (Qubit [int]): Qubit dónde se aplica la transformación

        Returns:
            RydbergQuantumCircuit: Circuito de Rydberg con Uxy(theta, phi) aplicada sobre 'qubit'

        """
        return self.append(RydbergUxyGate(theta, phi), [qubit])

    def cuxy(
        self,
        theta: float,
        phi: float,
        control_qubit: int,
        target_qubit: Union[int, List[int]],
    ):
        """
        Método que aplica la transformación Controled-Uxy(theta, phi) entre
        'control_qubit' como qubit de control y 'taget_qubit' como qubit objetivo.

        Args:
            theta (float): Ángulo de rotación theta
            phi (float): Ángulo de rotación phi
            control_qubit (Qubit [int]): Qubit de control
            target_qubit (Qubit [int]): Qubit objetivo

        Returns:
            RydbergQuantumCircuit: Circuito de Rydberg con CUxy(theta, phi) aplicada sobre
            'control_qubit' y 'target_qubit'

        """
        return self.append(RydbergCUxyGate(theta, phi), [control_qubit, target_qubit])

    def cp(
        self, phi11: float, qubit1: Union[int, List[int]], qubit2: Union[int, List[int]]
    ):
        """
        Método que aplica la transformación CPhase(phi11) entre
        'qubit1' y 'qubit2'.

        Args:
            phi11 (float): Ángulo de rotación phi11
            qubit1 (Qubit [int]): Qubit 1
            qubit2 (Qubit [int]): Qubit 2

        Returns:
            RydbergQuantumCircuit: Circuito de Rydberg con CPhase(phi11)
            aplicada sobre 'qubit1' y 'qubit2'.

        """
        return self.append(RydbergCPhase(phi11), [qubit1, qubit2])

    def xy(
        self, theta: float, qubit1: Union[int, List[int]], qubit2: Union[int, List[int]]
    ):
        """
        Método que aplica la transformación XY(theta) entre
        'qubit1' y 'qubit2'.

        Args:
            theta (float): Ángulo de rotación theta
            qubit1 (Qubit [int]): Qubit 1
            qubit2 (Qubit [int]): Qubit 2

        Returns:
            RydbergQuantumCircuit: Circuito de Rydberg con XY(theta)
            aplicada sobre 'qubit1' y 'qubit2'.

        """
        return self.append(RydbergXYGate(theta), [qubit1, qubit2])

    """Compuertas comunes a base de las basicas de Átomos de Rydberg"""

    def h(self, qubit: Union[int, List[int]]):
        """
        Método que aplica la transformación Hadamard sobre 'qubit'

        Args:
            qubit (Qubit [int]): Qubit donde se aplica la transformación

        Returns:
            RydbergQuantumCircuit: Circuito de Rydberg con Hadamard aplicada sobre
            'qubit'

        """
        return self.append(RydbergHGate(), [qubit])

    def rx(self, theta: float, qubit: Union[int, List[int]]):
        """
        Método que aplica la transformación Rotación en X sobre 'qubit'

        Args:
            theta (float): Ángulo de rotación sobre el eje X
            qubit (Qubit [int]): Qubit donde se aplica la transformación

        Returns:
            RydbergQuantumCircuit: Circuito de Rydberg con Rx(theta) aplicada sobre
            'qubit'

        """
        return self.append(RydbergRxGate(theta), [qubit])

    def ry(self, theta: float, qubit: Union[int, List[int]]):
        """
        Método que aplica la transformación Rotación en Y sobre 'qubit'

        Args:
            theta (float): Ángulo de rotación sobre el eje Y
            qubit (Qubit [int]): Qubit donde se aplica la transformación

        Returns:
            RydbergQuantumCircuit: Circuito de Rydberg con Ry(theta) aplicada sobre
            'qubit'

        """
        return self.append(RydbergRyGate(theta), [qubit])

    def rz(self, theta: float, qubit: Union[int, List[int]]):
        """
        Método que aplica la transformación Rotación en Z sobre 'qubit'

        Args:
            theta (float): Ángulo de rotación sobre el eje Z
            qubit (Qubit [int]): Qubit donde se aplica la transformación

        Returns:
            RydbergQuantumCircuit: Circuito de Rydberg con Rz(theta) aplicada sobre
            'qubit'

        """
        return self.append(RydbergRzGate(theta), [qubit])

    def cx(self, ctrl_qubit: int, target_qubit: Union[int, List[int]]):
        """
        Método que aplica la transformación Control-X o CNOT sobre 'control_qubit' y
        'target_qubit'

        Args:
            control_qubit (Qubit [int]): Qubit de control
            target_qubit (Qubit [int]): Qubit objetivo

        Returns:
            RydbergQuantumCircuit: Circuito de Rydberg con Control-X aplicada sobre
            'control_qubit' y 'target_qubit'
        """
        self.append(RydbergCUxyGate(np.pi, 0), [ctrl_qubit, target_qubit])

    def iswap(self, qubit1: int, qubit2: int):
        """
        Método que aplica la transformación Swap entre 'qubit1' y 'qubit2'

        Args:
            qubit1 (Qubit [int]): Primer qubit de SWAP
            qubit2 (Qubit [int]): Segundo qubit de SWAP

        Returns:
            RydbergQuantumCircuit: Circuito de Rydberg con SWAP aplicada entre
            'qubit1' y 'qubit2'
        """
        self.append(RydbergSwapGate(), [qubit1, qubit2])

    def swap(self, qubit1: int, qubit2: int):
        self.iswap(qubit1, qubit2)

    """QFT Circuit as Gate"""

    def qft(
        self,
        num_qubits: Optional[int] = None,
        approximation_degree: Optional[int] = 0,
        do_swaps: Optional[bool] = True,
        insert_barriers: Optional[bool] = True,
        name="qft",
    ):
        """
        Método que construye la subcircuito de QFT de 'num_qubits' a base de las
        transformaciones en átomos de Rydberg

        Args:
            num_qubits (int): Número de qubits de la QFT
            approximation_degree (int): Nivel de entrelazamiento de los estados en la QFT
            do_swapps (bool): Hacer o no los swaps finales de la QFT
            inverse (bool): Hacer o no el circuito inverso de la QFT
            inser_barries (bool): Insertar las barreras entre cada etapa del circuit
            name (str): Nombre del circuito

        Returns:
            RydbergQuantumCircuit: Modelo circuital cuántico de Rydberg con la QFT de 'num_qubits'
            aplicada
        """
        num_qubits = self.num_qubits

        if num_qubits == 0:
            return

        for j in reversed(range(num_qubits)):
            self.h(j)
            num_entanglements = max(
                0, j - max(0, approximation_degree - (num_qubits - j - 1))
            )
            for k in reversed(range(j - num_entanglements, j)):
                # Use negative exponents so that the angle safely underflows to zero, rather than
                # using a temporary variable that overflows to infinity in the worst case.
                lam = np.pi * (2.0 ** (k - j))
                self.cp(lam, j, k)

            if insert_barriers:
                self.barrier()

        if do_swaps:
            for i in range(num_qubits // 2):
                self.swap(i, num_qubits - i - 1)

        # wrapped = circuit.to_instruction() if insert_barriers else circuit.to_gate()
        # wrapped.name = 'QFT'
        # self.append(wrapped, range(num_qubits) , [])
