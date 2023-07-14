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
