import paddle.nn.functional as F

def get_activation(act_name: str) -> Callable:
    """Get activation function according to act_name.

    Args:
        act_name (str): Name of activation, such as "tanh".

    Returns:
        Callable: Paddle activation function.
    """
    activation_functions = {
        "relu": F.relu,
        "tanh": F.tanh,
        "sigmoid": F.sigmoid,
        "softmax": F.softmax,
        "leaky_relu": F.leaky_relu,
        "gelu": F.gelu,
    }

    if act_name not in activation_functions:
        raise ValueError(f"Unsupported activation function: {act_name}")

    return activation_functions[act_name]