def build_crit_dict(gates):
    crit_dict = {}
    for gate in gates:
        for input_node in gate.inputs:
            if input_node not in crit_dict:
                crit_dict[input_node] = set()
            crit_dict[input_node].add(gate)
    return crit_dict