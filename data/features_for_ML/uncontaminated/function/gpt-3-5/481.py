def get_activation(act_name: str) -> Callable:
    if act_name == "tanh":
        return paddle.nn.functional.tanh
    elif act_name == "sigmoid":
        return paddle.nn.functional.sigmoid
    elif act_name == "relu":
        return paddle.nn.functional.relu
    elif act_name == "softmax":
        return paddle.nn.functional.softmax
    else:
        raise ValueError("Activation function {} not supported".format(act_name))