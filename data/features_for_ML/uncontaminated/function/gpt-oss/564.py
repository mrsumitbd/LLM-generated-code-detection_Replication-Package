import torch
import torch.nn as nn
import torch.nn.functional as F

def instantiate_network(config):
    """
    Instantiate a PyTorch neural network based on a configuration dictionary.

    Expected config format:
        {
            "type": "mlp" | "cnn" | "custom",
            "input_dim": int,          # for mlp
            "output_dim": int,         # for mlp
            "layers": [                # list of layer configs
                {"type": "linear", "out_features": int, "activation": "relu" | "tanh" | ...},
                {"type": "conv2d", "out_channels": int, "kernel_size": int, "stride": int, "padding": int, "activation": ...},
                ...
            ],
            "activation": "relu" | "tanh" | ...  # default activation for layers without explicit activation
        }

    For "custom" type, the config must provide a callable under key "builder" that returns an nn.Module.
    """
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")

    net_type = config.get("type", "mlp").lower()
    default_activation = config.get("activation", None)

    # Helper to map activation string to nn.Module
    def _act(name):
        if name is None:
            return None
        name = name.lower()
        if name == "relu":
            return nn.ReLU()
        if name == "tanh":
            return nn.Tanh()
        if name == "sigmoid":
            return nn.Sigmoid()
        if name == "leakyrelu":
            return nn.LeakyReLU()
        if name == "gelu":
            return nn.GELU()
        if name == "softmax":
            return nn.Softmax(dim=1)
        # Default: identity
        return nn.Identity()

    if net_type == "custom":
        builder = config.get("builder")
        if not callable(builder):
            raise ValueError("Custom network requires a callable 'builder' in config")
        return builder()

    layers = []
    if net_type == "mlp":
        input_dim = config.get("input_dim")
        if input_dim is None:
            raise ValueError("MLP config must specify 'input_dim'")
        for idx, layer_cfg in enumerate(config.get("layers", [])):
            if layer_cfg.get("type") != "linear":
                raise ValueError(f"MLP layer {idx} must be of type 'linear'")
            out_features = layer_cfg.get("out_features")
            if out_features is None:
                raise ValueError(f"MLP layer {idx} missing 'out_features'")
            layers.append(nn.Linear(input_dim, out_features))
            act_name = layer_cfg.get("activation", default_activation)
            act = _act(act_name)
            if act is not None and not isinstance(act, nn.Identity):
                layers.append(act)
            input_dim = out_features
        # Final output layer
        output_dim = config.get("output_dim")
        if output_dim is not None:
            layers.append(nn.Linear(input_dim, output_dim))
    elif net_type == "cnn":
        # Expect input channels in config
        in_channels = config.get("input_channels", 3)
        for idx, layer_cfg in enumerate(config.get("layers", [])):
            ltype = layer_cfg.get("type")
            if ltype == "conv2d":
                out_channels = layer_cfg.get("out_channels")
                kernel_size = layer_cfg.get("kernel_size", 3)
                stride = layer_cfg.get("stride", 1)
                padding = layer_cfg.get("padding", 0)
                if out_channels is None:
                    raise ValueError(f"Conv2d layer {idx} missing 'out_channels'")
                layers.append(nn.Conv2d(in_channels, out_channels, kernel_size,
                                        stride=stride, padding=padding))
                act_name = layer_cfg.get("activation", default_activation)
                act = _act(act_name)
                if act is not None and not isinstance(act, nn.Identity):
                    layers.append(act)
                in_channels = out_channels
            elif ltype == "maxpool2d":
                kernel_size = layer_cfg.get("kernel_size", 2)
                stride = layer_cfg.get("stride", kernel_size)
                layers.append(nn.MaxPool2d(kernel_size, stride))
            elif ltype == "flatten":
                layers.append(nn.Flatten())
            elif ltype == "linear":
                out_features = layer_cfg.get("out_features")
                if out_features is None:
                    raise ValueError(f"Linear layer {idx} missing 'out_features'")
                layers.append(nn.Linear(in_channels, out_features))
                act_name = layer_cfg.get("activation", default_activation)
                act = _act(act_name)
                if act is not None and not isinstance(act, nn.Identity):
                    layers.append(act)
                in_channels = out_features
            else:
                raise ValueError(f"Unsupported CNN layer type: {ltype}")
    else:
        raise ValueError(f"Unsupported network type: {net_type}")

    return nn.Sequential(*layers)