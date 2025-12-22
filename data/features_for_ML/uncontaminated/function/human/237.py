def build_crit_dict(gates):
    crit_dict = {}
    for id, qubits in gates.items():
        dependent = get_dependent_gates((id, qubits), gates)
        depths = get_depth_by_qubit(dependent)
        crit_path = max(depths.get(q, 0) for q in qubits)
        crit_dict[id] = crit_path
    return crit_dict