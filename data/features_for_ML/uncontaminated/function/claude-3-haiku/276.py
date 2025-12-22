import numpy as np

def rand_gumbel_like(x):
    """
    Generate a random number following a Gumbel-like distribution.

    Args:
        x (float): The input value to use for generating the random number.

    Returns:
        float: A random number following a Gumbel-like distribution.
    """
    return -np.log(-np.log(np.random.uniform(0, 1))) * x