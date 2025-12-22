import numpy as np

def get_continuous_action(d_acts, c_act_max, c_act_min, n_bins):
    """
    Discretize a continuous action space into a fixed number of bins.

    Args:
        d_acts (int): The number of discrete actions.
        c_act_max (float): The maximum value of the continuous action space.
        c_act_min (float): The minimum value of the continuous action space.
        n_bins (int): The number of bins to divide the continuous action space into.

    Returns:
        np.ndarray: An array of continuous action values, one for each discrete action.
    """
    bin_size = (c_act_max - c_act_min) / n_bins
    bin_centers = np.linspace(c_act_min + bin_size / 2, c_act_max - bin_size / 2, n_bins)
    return bin_centers