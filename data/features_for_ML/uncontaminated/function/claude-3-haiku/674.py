import numpy as np
from scipy.stats import t

def _compute_mean_and_conf_int(val):
    """
    Compute the mean and confidence interval of the input values.

    Args:
        val (numpy.ndarray): A 1D numpy array of values.

    Returns:
        tuple: A tuple containing the mean and the confidence interval (lower, upper).
    """
    mean = np.mean(val)
    std_err = np.std(val) / np.sqrt(len(val))
    t_value = t.ppf(0.975, len(val) - 1)
    conf_int = (mean - t_value * std_err, mean + t_value * std_err)
    return mean, conf_int