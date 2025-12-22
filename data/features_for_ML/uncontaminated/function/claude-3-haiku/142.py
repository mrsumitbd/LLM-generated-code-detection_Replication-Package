import numpy as np

def fluid_field_weights_gravity(value):
    """
    Calculates the fluid field weights for a given value.

    Args:
        value (float): The input value.

    Returns:
        numpy.ndarray: The fluid field weights.
    """
    weights = np.array([
        1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0,
        1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0
    ])
    gravity = np.array([0.0, 0.0, -value])
    return weights * gravity