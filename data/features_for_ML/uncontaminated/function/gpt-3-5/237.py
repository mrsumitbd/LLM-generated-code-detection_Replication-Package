def build_crit_dict(gates):
    crit_dict = {}
    for gate in gates:
        crit_dict[gate] = len(gate)
    return crit_dict