def get_activation(act_name: str) -> Callable:
    """Get activation function according to act_name.

    Args:
        act_name (str): Name of activation, such as "tanh".

    Returns:
        Callable: Paddle activation function.
    """
    import paddle.nn.functional as F
    
    activation_dict = {
        'tanh': F.tanh,
        'relu': F.relu,
        'sigmoid': F.sigmoid,
        'softmax': F.softmax,
        'elu': F.elu,
        'selu': F.selu,
        'prelu': F.prelu,
        'gelu': F.gelu,
        'swish': F.swish,
        'mish': F.mish,
        'softplus': F.softplus,
        'softsign': F.softsign,
        'leaky_relu': F.leaky_relu,
        'hard_sigmoid': F.hard_sigmoid,
        'hard_swish': F.hard_swish,
        'hard_tanh': F.hard_tanh,
        'log_softmax': F.log_softmax,
        'softmax': F.softmax,
        'glu': F.glu,
        'celu': F.celu,
        'relu6': F.relu6,
        'none': lambda x: x,
    }
    
    act_name_lower = act_name.lower() if act_name else 'none'
    
    if act_name_lower in activation_dict:
        return activation_dict[act_name_lower]
    else:
        raise ValueError(f"Unsupported activation function: {act_name}")