def apply_gate(x, gate, tr_gate=None, tr_token=None):
    if gate == 'X':
        return 1 - x
    elif gate == 'Z':
        return -x
    elif gate == 'H':
        return (1 / (2 ** 0.5)) * (1 - 1j * x)
    elif gate == 'T':
        return (1 + 1j * (2 ** 0.5 - 1)) * x
    elif gate == 'CNOT':
        if tr_gate is None or tr_token is None:
            raise ValueError("tr_gate and tr_token are required for CNOT gate")
        return x * tr_gate + (1 - x) * tr_token
    else:
        raise ValueError("Invalid gate specified")