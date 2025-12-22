from typing import Callable
import paddle.nn.functional as F


def get_activation(act_name: str) -> Callable:
    """Get activation function according to act_name.

    Args:
        act_name (str): Name of activation, such as "tanh".

    Returns:
        Callable: Paddle activation function.
    """
    act_name = act_name.lower().strip()
    # Identity / no activation
    if act_name in {"none", "identity", "linear"}:
        return lambda x: x

    # Mapping of common activation names to Paddle functions
    act_map = {
        "relu": F.relu,
        "sigmoid": F.sigmoid,
        "tanh": F.tanh,
        "leaky_relu": F.leaky_relu,
        "gelu": F.gelu,
        "softmax": F.softmax,
        "softplus": F.softplus,
        "softsign": F.softsign,
        "selu": F.selu,
        "elu": F.elu,
        "hard_swish": F.hard_swish,
        "hard_sigmoid": F.hard_sigmoid,
        "swish": F.swish,
        "silu": F.silu,
        "mish": F.mish,
    }

    if act_name not in act_map:
        raise ValueError(
            f"Unsupported activation '{act_name}'. "
            f"Supported activations: {sorted(act_map.keys())}"
        )

    return act_map[act_name]