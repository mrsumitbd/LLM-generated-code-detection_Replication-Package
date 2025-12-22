def build_crit_dict(gates):
    """
    Compute the critical path length for each gate in a quantum circuit.

    Parameters
    ----------
    gates : list
        A list of gate objects or dictionaries. Each gate must provide:
        - a list of qubits it acts on, accessible via `gate.qubits` or
          `gate.targets` (or the dictionary keys 'qubits' / 'targets').
        - an optional duration, accessible via `gate.duration` or the
          dictionary key 'duration'. If not provided, a default duration
          of 1 is used.

    Returns
    -------
    dict
        A dictionary mapping each gate to its critical path length
        (the longest path from the start of the circuit to that gate,
        including its own duration).
    """
    # Helper to extract attributes from a gate (object or dict)
    def _get_attr(g, name, default=None):
        if isinstance(g, dict):
            return g.get(name, default)
        return getattr(g, name, default)

    # Map each qubit to the last gate that acted on it
    last_gate_on_qubit = {}
    crit_dict = {}

    for gate in gates:
        # Determine qubits and duration
        qubits = _get_attr(gate, "qubits", _get_attr(gate, "targets", []))
        duration = _get_attr(gate, "duration", 1)

        # Compute the maximum critical path length among predecessors
        max_pred = 0
        for q in qubits:
            pred_gate = last_gate_on_qubit.get(q)
            if pred_gate is not None:
                max_pred = max(max_pred, crit_dict[pred_gate])

        # Critical path length for this gate
        crit_len = max_pred + duration
        crit_dict[gate] = crit_len

        # Update last gate for each qubit
        for q in qubits:
            last_gate_on_qubit[q] = gate

    return crit_dict