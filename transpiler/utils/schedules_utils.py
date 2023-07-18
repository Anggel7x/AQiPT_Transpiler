import numpy as np
from typing import List

def merge_pulses(pulses :dict, name: str):
            coupling = {}
            done = []
            k = 0

            values = list(pulses.values())
            for i in range(len(values)):
                if i in done: continue
                v1 = values[i]

                for j in range(len(values)):
                    
                    if i == j: continue
                    
                    v2 = values[j]

                    # Matching the same levels of coupling
                    if v2[0] == v1[0]:
                        v1 = [v1[0], v1[1], np.add(v1[2], v2[2])]
                        values[i] = v1
                        done.append(j)

                coupling[name+str(k)] = v1
                done.append(i)
                k += 1

            return coupling
        
def coupling_detuning_constructors(couplings: List[float], detunings : List[float], omega_coup = 20, omega_detu = 0) -> tuple():
    coupling1 = {}
    
    if isinstance(omega_coup, (int,float)) :
    
        for i, coupling in enumerate(couplings):
            levels , coupling = coupling
            coupling1['Coupling'+str(i)] = [levels, omega_coup, coupling]
            
    elif isinstance(omega_coup, List):
        assert len(omega_coup) == len(couplings)
        
        for i, coupling in enumerate(couplings):
            levels , coupling = coupling
            coupling1['Coupling'+str(i)] = [levels, omega_coup[i], coupling]

    detuning1 = {}
    for i, detuning in enumerate(detunings):
        levels , detuning = detuning
        detuning1['Detuning'+str(i)] = [levels, omega_detu, detuning]
        
    return coupling1, detuning1


def freq_given_phi(phi : float, Vct : float):
    freq = + Vct * 8.96698 * np.log(-0.361329*(0.374038 - phi))/(2*np.pi)
    return freq
    