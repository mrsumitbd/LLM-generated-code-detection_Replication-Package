def get_norm_module(module: nn.Module, causal: bool = False, norm: str = "none", **norm_kwargs) -> nn.Module:
    if norm == "none":
        return module
    elif norm == "batch":
        return nn.BatchNorm1d(**norm_kwargs)
    elif norm == "layer":
        return nn.LayerNorm(**norm_kwargs)
    elif norm == "instance":
        return nn.InstanceNorm1d(**norm_kwargs)
    else:
        raise ValueError(f"Unsupported normalization type: {norm}")