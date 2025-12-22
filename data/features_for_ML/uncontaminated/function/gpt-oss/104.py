import numpy as np

def apply_gate(x, gate, tr_gate=None, tr_token=None):
    """
    Apply a quantum gate (or a callable) to a state vector `x`.

    Parameters
    ----------
    x : array_like
        State vector (1‑D array) or matrix (2‑D array) to which the gate is applied.
    gate : array_like or str or callable
        The gate to apply. It can be:
        * a NumPy array (matrix) representing the gate,
        * a string identifier for a common single‑qubit gate,
        * a callable that accepts the state vector and returns the transformed state.
    tr_gate : array_like or str or callable, optional
        A transformation gate to apply *before* `gate`. If provided, it is applied
        to `x` first. The same type rules as `gate` apply.
    tr_token : any, optional
        If provided and `tr_gate` is a string, the transformation is applied only
        if `tr_token` matches the string. This is a very light‑weight conditional
        mechanism; otherwise the transformation is applied unconditionally.

    Returns
    -------
    ndarray
        The transformed state vector.
    """
    # Helper to convert gate spec to matrix
    def _gate_to_matrix(g):
        if callable(g):
            return g
        if isinstance(g, str):
            g = g.upper()
            if g == "X":
                return np.array([[0, 1], [1, 0]], dtype=complex)
            if g == "Y":
                return np.array([[0, -1j], [1j, 0]], dtype=complex)
            if g == "Z":
                return np.array([[1, 0], [0, -1]], dtype=complex)
            if g == "H":
                return 1/np.sqrt(2) * np.array([[1, 1], [1, -1]], dtype=complex)
            if g == "S":
                return np.array([[1, 0], [0, 1j]], dtype=complex)
            if g == "T":
                return np.array([[1, 0], [0, np.exp(1j*np.pi/4)]], dtype=complex)
            # Add more gates as needed
            raise ValueError(f"Unknown gate string: {g}")
        # Assume array_like
        arr = np.asarray(g, dtype=complex)
        if arr.ndim == 1:
            # Treat as diagonal gate
            return np.diag(arr)
        return arr

    # Convert input to numpy array
    state = np.asarray(x, dtype=complex)

    # Apply transformation gate if provided
    if tr_gate is not None:
        # Conditional application based on tr_token
        if tr_token is not None and isinstance(tr_gate, str):
            if tr_token != tr_gate.upper():
                # Skip transformation
                pass
            else:
                tr_func = _gate_to_matrix(tr_gate)
                if callable(tr_func):
                    state = tr_func(state)
                else:
                    state = tr_func @ state
        else:
            tr_func = _gate_to_matrix(tr_gate)
            if callable(tr_func):
                state = tr_func(state)
            else:
                state = tr_func @ state

    # Apply main gate
    gate_func = _gate_to_matrix(gate)
    if callable(gate_func):
        return gate_func(state)
    else:
        return gate_func @ state