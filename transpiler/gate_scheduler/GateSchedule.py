def coupling_detuning_constructors(couplings: List, detunings : List, omega_coup : 20, omega_detu = 0) -> tuple():
    coupling1 = {}
    for i, coupling in enumerate(couplings):
        levels , coupling = coupling
        coupling1['Coupling'+str(i)] = [levels, omega_coup, coupling]


    detuning1 = {}
    for i, detuning in enumerate(detunings):
        levels , detuning = detuning
        detuning1['Detuning'+str(i)] = [levels, omega_detu, detuning]
        
    return coupling1, detuning1
