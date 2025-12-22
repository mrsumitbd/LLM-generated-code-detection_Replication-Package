from typing import Callable

def get_activation(act_name: str) -> Callable:
    """Get activation function according to act_name.

    Args:
        act_name (str): Name of activation, such as "tanh".

    Returns:
        Callable: Paddle activation function.
    """
    if act_name.lower() not in act_func_dict:
        raise ValueError(f"act_name({act_name}) not found in act_func_dict")

    act_layer = act_func_dict[act_name.lower()]
    if isinstance(act_layer, type) and act_name != "stan":
        # Is a activation class but not a instance of it, instantiate manually(except for 'Stan')
        return act_layer()

    return act_layer