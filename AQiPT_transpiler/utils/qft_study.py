import time
import numpy as np
from qiskit import *
from qiskit.visualization import plot_bloch_multivector
from IPython.display import display, clear_output

#Nakahara way of QFT
def dec2bin(val):
    '''
        Function that yields the binary value of an decimal number input
        
        INPUTS:
        ------
            val(int): decimal integer value to be transform
            
        OUTPUTS:
        -------
            binary int
    '''
    
    s = bin(val)[2:] # Ésto remueve el prefijo "0b" del string que devuelve la función "bin"
    return s[::-1]

def swapping(qc):
    '''
        Function that yields a quantum circuit with swap gates betwenn first
        to half integer number of qubits
        
        INPUTS:
        -------
            qc (quantum circuit): qiskit quantum circuit that series of swap gates 
                                   for the half of the qubits in the circuit
        
        OUTPUTS:
        -------
            quantum circuit qiskit object
        
    '''
    
    n = qc.num_qubits # Obtenemos la cantidad exacta de qubits en el registro cuántico
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1) # Hacemos el swap hasta llegar a la mitad entera, si hay 3 qubits entonces éste sera 1
    return qc

def Bjk(qc, n, barrierON=True):
    '''
        Recursive function for adding the specific rotation in each of the qubits
        
        INPUTS:
        ------
            qc (quantum circuit):
            n (int): number of qubits, used as iterator
            barrierON (bool): boolean for including barriers
            
        OUTPUTS:
        --------
            quantum circuit qiskit object
            
    '''
    if n == 0: # Estado de salida de la función para el caso final
        return qc
    
    if barrierON is True:
        qc.barrier(); #including barriers

    qc.h(qc.num_qubits-n) # Realizamos la puerta H aca para evitar una operación
    n -= 1 # Reducimos el iterador
    for qubit in range(qc.num_qubits-n, qc.num_qubits):
        qc.cp(2*np.pi/2**(qubit-(qc.num_qubits-n-1)+1), qubit, qc.num_qubits-n-1) # k=qubit, j=qc.num_qubits-(n+1)
    # Al final de la función, la volvemos a invocar para realizar
    # la siguiente iteración con el nuevo n.
    Bjk(qc, n)

def QFT_NKHR(state, n, barrierON=True):
    '''
        Function that yields the Quantum Fourier Transform of a string state (Method shown by Nakahara)
        
        INPUTS:
        ------
            state (int): search element
            n (int): transform order
            barrierON (bool): boolean for including barriers
            
        OUTPUTS:
        --------
            quantum circuit qiskit object
            
    '''
    assert state < 2**n
    
    bin_state = dec2bin(state)
    
    qc = QuantumCircuit(n)
    for i in range(len(bin_state)):
        if bin_state[i]=='1': qc.x(i)
            
    swapping(qc)
    Bjk(qc,n, barrierON)
    return qc

# Qiskit way of QFT
def ContRot(qc, n, barrierON=True):
    '''
        Function that yields a quantum circuit including control rotations
    '''
    
    if barrierON is True:
        qc.barrier(); #including barriers
        
    if n == 0: 
        return qc #returns the quantum circuit in the last case
    
    n -= 1; #iterator
    qc.h(n); #including 
    for qubit in range(n-1, -1, -1):
        qc.cp(2*np.pi/2**(n-qubit+1), qubit, n); # CPHASE(theta, qubit_k, qubit_j)

    ContRot(qc, n); #adding rotations
    
def QFT_IBM(state, n, barrier=True):
    '''
        Function that yields the Quantum Fourier Transform of a string state (method shown by Qiskit)
        
        INPUTS:
        ------
            state (int): search element
            n (int): transform order
            barrierON (bool): boolean for including barriers
            
        OUTPUTS:
        --------
            quantum circuit qiskit object
            
    '''
    assert state < 2**n; #raise exception error
    
    bin_x = dec2bin(state);  #converting to binary
    
    qc = QuantumCircuit(n); #creating qiskit quantum circuit
    for i in range(len(bin_x)):
        if bin_x[i]=='1': qc.x(i); #adding initial rotations
    
    ContRot(qc, n, barrier); #adding control rotations
    swapping(qc); #swapping qubits
    return qc

def Animate_QC(QFT_f, n):
    '''
        Function that yields animation on the state vector in the block sphere
        
        INPUTS:
        ------
            QFT_f (function): Quantum Fourier Function transform
            n (int): tranform order
        
    '''
    for i in range(2**n):
        clear_output(wait=True);
        qft = QFT_f(i, n);
        display(plot_bloch_multivector(qft));
        time.sleep(0.3);