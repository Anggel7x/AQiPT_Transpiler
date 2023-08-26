from typing import List, Tuple, Union
import numpy as np


def merge_pulses(pulses: dict, name: str) -> dict:
    r"""Esta función une todas las descripciones funcionales de los
    pulsos en una sola.

    Args:
        pulses (dict): Pulsos que se van a unir.
        name (str): Nombre del pulso donde se van a contener.

    Returns:
        dict: Acoples unidos.
    """
    coupling = {}
    done = []
    k = 0

    values = list(pulses.values())
    for i, vi in enumerate(values):
        if i in done:
            continue
        v1 = vi

        for j, vj in enumerate(values):
            if i == j:
                continue

            v2 = vj

            # Matching the same levels of coupling
            if v2[0] == v1[0] and v2[1] == v1[1]:
                v1 = [v1[0], v1[1], np.add(v1[2], v2[2])]
                vi = v1
                done.append(j)

        coupling[name + str(k)] = v1
        done.append(i)
        k += 1

    return coupling


def coupling_detuning_constructors(
    couplings: List[tuple],
    detunings: List[tuple],
    omega_coup: Union[List[float], float, int] = 20,
    omega_detu: Union[List[float], float, int] = 0,
) -> Tuple[dict, dict]:
    r"""Función que construye las descripción en diccionartio de los
    couplings y detunings.

    Args:
        couplings (List[float]): Lista que contiene todos los acoples con sus
        pares y funciones
        detunings (List[float]): Lista que contiene todos las desintonizaciones con sus
        pares y funciones
        omega_coup (int, optional): Intensidad del acople. Defaults to 20.
        omega_detu (int, optional): Intensidad de la desintonización. Defaults to 0.

    Returns:
        Tuple[dict, dict]: Par de diccionarios que contienen los couplings
        y detunings ya construidos.
    """
    coupling1 = {}

    if isinstance(omega_coup, (int, float)):
        for i, coupling in enumerate(couplings):
            levels, coupling = coupling
            coupling1["Coupling" + str(i)] = [levels, omega_coup, coupling]

    elif isinstance(omega_coup, List):
        assert len(omega_coup) == len(couplings)

        for i, coupling in enumerate(couplings):
            levels, coupling = coupling
            coupling1["Coupling" + str(i)] = [levels, omega_coup[i], coupling]

    detuning1 = {}
    for i, detuning in enumerate(detunings):
        levels, detuning = detuning
        detuning1["Detuning" + str(i)] = [levels, omega_detu, detuning]

    return coupling1, detuning1


def freq_given_phi(phi: float, v_ct: float) -> float:
    r"""Función que retorna la frecuencia necesaria para generar un angulo
    $\Phi_{11}$ bajo la intensidad de interaccion $V_{ct}$.

    Args:
        phi (float): Angulo requerido.
        v_ct (float): Intensidad de la interaccioón.

    Returns:
        float: Frecuencia calculada.
    """
    phi = max(phi, np.pi / 8)
    phi = min(phi, 0.9 * np.pi)
    freq = +v_ct * 9.55717 * np.log(-0.3614 * (0.3745 - phi)) / (2 * np.pi)
    return freq
