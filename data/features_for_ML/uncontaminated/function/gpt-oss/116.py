import pathlib
from typing import Dict, Any

import torch
try:
    from safetensors.torch import load_file as safe_load_file
except ImportError:
    safe_load_file = None


# Define a type alias for clarity; adjust if a specific class is used elsewhere.
IPAdapterStateDict = Dict[str, torch.Tensor]


def load_ip_adapter_tensors(ip_adapter_ckpt_path: pathlib.Path, device: str) -> IPAdapterStateDict:
    """
    Load an IP-Adapter checkpoint and return its state dictionary on the specified device.

    Parameters
    ----------
    ip_adapter_ckpt_path : pathlib.Path
        Path to the checkpoint file (.pt, .bin, or .safetensors).
    device : str
        Target device for the tensors (e.g., 'cpu', 'cuda', 'cuda:0').

    Returns
    -------
    IPAdapterStateDict
        Dictionary mapping parameter names to tensors on the requested device.
    """
    if not ip_adapter_ckpt_path.is_file():
        raise FileNotFoundError(f"Checkpoint file not found: {ip_adapter_ckpt_path}")

    # Determine file extension
    suffix = ip_adapter_ckpt_path.suffix.lower()

    # Load using safetensors if available and appropriate
    if suffix == ".safetensors":
        if safe_load_file is None:
            raise ImportError(
                "safetensors package is required to load .safetensors files. "
                "Install it via `pip install safetensors`."
            )
        state_dict = safe_load_file(str(ip_adapter_ckpt_path), device=device)
    else:
        # For .pt/.bin or other formats, use torch.load
        state_dict = torch.load(
            str(ip_adapter_ckpt_path),
            map_location=device,
            weights_only=True,
        )

    # Some checkpoints wrap the state dict under a 'state_dict' key
    if isinstance(state_dict, dict) and "state_dict" in state_dict:
        state_dict = state_dict["state_dict"]

    # Ensure all tensors are on the requested device
    if isinstance(state_dict, dict):
        for k, v in state_dict.items():
            if isinstance(v, torch.Tensor):
                state_dict[k] = v.to(device)

    return state_dict