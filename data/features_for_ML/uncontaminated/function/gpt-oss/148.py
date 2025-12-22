import numpy as np

def get_continuous_action(d_acts, c_act_max, c_act_min, n_bins):
    """
    Map discrete action indices to continuous action values.

    Parameters
    ----------
    d_acts : int, float, array-like
        Discrete action indices. Expected to be in the range [0, n_bins-1].
    c_act_max : float
        Maximum value of the continuous action space.
    c_act_min : float
        Minimum value of the continuous action space.
    n_bins : int
        Number of discrete bins (size of the discrete action space).

    Returns
    -------
    c_acts : float or ndarray
        Continuous action values mapped from the discrete indices.
    """
    # Convert input to numpy array for vectorised operations
    d_arr = np.asarray(d_acts, dtype=float)

    # Clip discrete actions to valid range
    d_arr = np.clip(d_arr, 0, n_bins - 1)

    # Normalise discrete indices to [0, 1]
    norm = d_arr / (n_bins - 1)

    # Scale to continuous action range
    c_arr = c_act_min + norm * (c_act_max - c_act_min)

    # Preserve original shape: if input was scalar, return scalar
    if np.isscalar(d_acts):
        return float(c_arr)
    return c_arr