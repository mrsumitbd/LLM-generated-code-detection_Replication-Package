from typing import Callable
import numpy as np

def get_activation_function(activation_function: str, inverse: bool = False) -> Callable:
    """
    Return an activation function or its inverse based on the provided name.

    Parameters
    ----------
    activation_function : str
        Name of the activation function. Supported names (case-insensitive):
        'relu', 'sigmoid', 'tanh', 'softmax', 'linear', 'leaky_relu',
        'elu', 'selu', 'gelu', 'softplus', 'softsign', 'hard_sigmoid',
        'swish', 'mish', 'logistic', 'identity', 'none'.

    inverse : bool, optional
        If True, return the inverse of the activation function when defined.
        Raises ValueError if the inverse is not defined.

    Returns
    -------
    Callable
        A function that accepts a scalar or NumPy array and returns the
        activation (or its inverse) applied element-wise.

    Raises
    ------
    ValueError
        If the activation name is unknown or the inverse is not defined.
    """
    name = activation_function.lower()

    # ---------- Activation functions ----------
    def relu(x):
        return np.maximum(0, x)

    def sigmoid(x):
        return 1.0 / (1.0 + np.exp(-x))

    def tanh(x):
        return np.tanh(x)

    def softmax(x):
        # Subtract max for numerical stability
        shiftx = x - np.max(x, axis=-1, keepdims=True)
        exps = np.exp(shiftx)
        return exps / np.sum(exps, axis=-1, keepdims=True)

    def linear(x):
        return x

    def leaky_relu(x, alpha=0.01):
        return np.where(x > 0, x, alpha * x)

    def elu(x, alpha=1.0):
        return np.where(x > 0, x, alpha * (np.exp(x) - 1))

    def selu(x, lam=1.0507, alpha=1.67326):
        return lam * np.where(x > 0, x, alpha * (np.exp(x) - 1))

    def gelu(x):
        return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))

    def softplus(x):
        return np.log1p(np.exp(x))

    def softsign(x):
        return x / (1 + np.abs(x))

    def hard_sigmoid(x):
        return np.clip(0.2 * x + 0.5, 0, 1)

    def swish(x):
        return x * sigmoid(x)

    def mish(x):
        return x * np.tanh(gelu(x))

    def logistic(x):
        return sigmoid(x)

    def identity(x):
        return x

    # ---------- Inverse functions ----------
    def inv_sigmoid(x):
        return np.log(x / (1 - x))

    def inv_tanh(x):
        return 0.5 * np.log((1 + x) / (1 - x))

    def inv_leaky_relu(x, alpha=0.01):
        return np.where(x > 0, x, x / alpha)

    def inv_elu(x, alpha=1.0):
        return np.where(x > 0, x, np.log(x / alpha + 1))

    def inv_selu(x, lam=1.0507, alpha=1.67326):
        return np.where(x > 0, x / lam, np.log(x / (lam * alpha) + 1))

    def inv_softplus(x):
        return np.log(np.exp(x) - 1)

    def inv_softsign(x):
        # Piecewise inverse for softsign
        return np.where(
            x >= 0,
            x / (1 - x),
            x / (1 + x)
        )

    def inv_hard_sigmoid(x):
        return (x - 0.5) / 0.2

    def inv_identity(x):
        return x

    def inv_linear(x):
        return x

    # Mapping dictionaries
    act_map = {
        'relu': relu,
        'sigmoid': sigmoid,
        'tanh': tanh,
        'softmax': softmax,
        'linear': linear,
        'leaky_relu': leaky_relu,
        'elu': elu,
        'selu': selu,
        'gelu': gelu,
        'softplus': softplus,
        'softsign': softsign,
        'hard_sigmoid': hard_sigmoid,
        'swish': swish,
        'mish': mish,
        'logistic': logistic,
        'identity': identity,
        'none': identity,
    }

    inv_map = {
        'sigmoid': inv_sigmoid,
        'tanh': inv_tanh,
        'leaky_relu': inv_leaky_relu,
        'elu': inv_elu,
        'selu': inv_selu,
        'softplus': inv_softplus,
        'softsign': inv_softsign,
        'hard_sigmoid': inv_hard_sigmoid,
        'identity': inv_identity,
        'linear': inv_linear,
    }

    if inverse:
        if name not in inv_map:
            raise ValueError(f"Inverse not defined for activation '{activation_function}'.")
        return inv_map[name]
    else:
        if name not in act_map:
            raise ValueError(f"Unknown activation function '{activation_function}'.")
        return act_map[name]