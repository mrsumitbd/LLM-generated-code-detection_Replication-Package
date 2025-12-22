def get_norm_module(
    module: nn.Module, causal: bool = False, norm: str = "none", **norm_kwargs
) -> nn.Module:
    """Return the proper normalization module. If causal is True, this will ensure the returned
    module is causal, or return an error if the normalization doesn't support causal evaluation.
    """
    if norm == "none":
        return nn.Identity()
    elif norm == "batch":
        if causal:
            raise ValueError("BatchNorm does not support causal evaluation")
        return nn.BatchNorm1d(module.out_channels if hasattr(module, 'out_channels') else module.out_features, **norm_kwargs)
    elif norm == "layer":
        return nn.LayerNorm(module.out_channels if hasattr(module, 'out_channels') else module.out_features, **norm_kwargs)
    elif norm == "instance":
        if causal:
            raise ValueError("InstanceNorm does not support causal evaluation")
        return nn.InstanceNorm1d(module.out_channels if hasattr(module, 'out_channels') else module.out_features, **norm_kwargs)
    elif norm == "group":
        if causal:
            raise ValueError("GroupNorm does not support causal evaluation")
        num_channels = module.out_channels if hasattr(module, 'out_channels') else module.out_features
        num_groups = norm_kwargs.pop('num_groups', 32)
        return nn.GroupNorm(num_groups, num_channels, **norm_kwargs)
    else:
        raise ValueError(f"Unknown normalization type: {norm}")