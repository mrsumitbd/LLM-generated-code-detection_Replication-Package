import numpy as np
from typing import Callable

def get_activation_function(activation_function: str, inverse=False) -> Callable:
    """
    Returns the specified activation function or its inverse.

    Args:
        activation_function (str): The name of the activation function.
        inverse (bool, optional): If True, returns the inverse of the activation function. Defaults to False.

    Returns:
        Callable: The activation function or its inverse.
    """
    activation_functions = {
        'sigmoid': (lambda x: 1 / (1 + np.exp(-x)), lambda x: x * (1 - x)),
        'tanh': (np.tanh, lambda x: 1 - np.tanh(x) ** 2),
        'relu': (lambda x: np.maximum(0, x), lambda x: (x > 0).astype(float)),
        'leaky_relu': (lambda x: np.maximum(0.01 * x, x), lambda x: (x > 0).astype(float) * 0.01 + (x <= 0).astype(float) * 0.01),
        'softmax': (lambda x: np.exp(x) / np.sum(np.exp(x), axis=-1, keepdims=True), lambda x: x - np.expand_dims(np.mean(x, axis=-1), axis=-1)),
    }

    if activation_function not in activation_functions:
        raise ValueError(f"Invalid activation function: {activation_function}")

    func, inverse_func = activation_functions[activation_function]
    return inverse_func if inverse else func