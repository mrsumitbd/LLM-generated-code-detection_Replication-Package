def update_param_fn(name: str, param: torch.Tensor) -> torch.Tensor:
    if 'weight' in name:
        return param * 0.99
    elif 'bias' in name:
        return param * 0.95
    else:
        return param