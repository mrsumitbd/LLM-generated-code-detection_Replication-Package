def get_activation_function(activation_function: str, inverse=False) -> Callable:
    import numpy as np

    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def relu(x):
        return np.maximum(0, x)

    def tanh(x):
        return np.tanh(x)

    def softmax(x):
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

    if activation_function == 'sigmoid':
        if inverse:
            return lambda x: x * (1 - x)
        else:
            return sigmoid
    elif activation_function == 'relu':
        if inverse:
            return lambda x: np.where(x > 0, 1, 0)
        else:
            return relu
    elif activation_function == 'tanh':
        if inverse:
            return lambda x: 1 - x**2
        else:
            return tanh
    elif activation_function == 'softmax':
        if inverse:
            raise ValueError("Inverse not supported for softmax activation function.")
        else:
            return softmax
    else:
        raise ValueError("Invalid activation function specified.")