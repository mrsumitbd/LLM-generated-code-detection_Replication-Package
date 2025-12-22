import math
from typing import Callable

def get_activation_function(activation_function: str, inverse=False) -> Callable:
    """
    Returns an activation function or its inverse based on the provided name.
    
    Args:
        activation_function: Name of the activation function ('relu', 'sigmoid', 'tanh', 'linear')
        inverse: If True, returns the inverse function
        
    Returns:
        A callable activation function or its inverse
    """
    
    if activation_function.lower() == 'relu':
        if inverse:
            def inverse_relu(x):
                return max(0, x)
            return inverse_relu
        else:
            def relu(x):
                return max(0, x)
            return relu
    
    elif activation_function.lower() == 'sigmoid':
        if inverse:
            def inverse_sigmoid(x):
                # Clamp x to avoid log(0) or log(negative)
                x = max(1e-7, min(1 - 1e-7, x))
                return math.log(x / (1 - x))
            return inverse_sigmoid
        else:
            def sigmoid(x):
                return 1 / (1 + math.exp(-x))
            return sigmoid
    
    elif activation_function.lower() == 'tanh':
        if inverse:
            def inverse_tanh(x):
                # Clamp x to avoid log(0) or log(negative)
                x = max(-1 + 1e-7, min(1 - 1e-7, x))
                return 0.5 * math.log((1 + x) / (1 - x))
            return inverse_tanh
        else:
            def tanh(x):
                return math.tanh(x)
            return tanh
    
    elif activation_function.lower() == 'linear':
        if inverse:
            def inverse_linear(x):
                return x
            return inverse_linear
        else:
            def linear(x):
                return x
            return linear
    
    else:
        raise ValueError(f"Unknown activation function: {activation_function}")