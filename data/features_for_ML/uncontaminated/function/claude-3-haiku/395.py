import torch.nn as nn

def get_norm_module(
    module: nn.Module, causal: bool = False, norm: str = "none", **norm_kwargs
) -> nn.Module:
    if norm == "none":
        return module
    elif norm == "batch_norm":
        if causal:
            raise ValueError("Batch normalization does not support causal evaluation.")
        return nn.BatchNorm1d(module.in_features, **norm_kwargs)
    elif norm == "layer_norm":
        return nn.LayerNorm(module.in_features, **norm_kwargs)
    elif norm == "group_norm":
        if causal:
            raise ValueError("Group normalization does not support causal evaluation.")
        return nn.GroupNorm(num_groups=norm_kwargs.get("num_groups", 1), num_channels=module.in_features, **norm_kwargs)
    elif norm == "instance_norm":
        if causal:
            raise ValueError("Instance normalization does not support causal evaluation.")
        return nn.InstanceNorm1d(module.in_features, **norm_kwargs)
    else:
        raise ValueError(f"Unsupported normalization type: {norm}")