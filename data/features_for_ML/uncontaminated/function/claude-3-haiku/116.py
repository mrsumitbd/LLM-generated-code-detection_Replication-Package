import torch
import pathlib
from typing import Dict, Tuple

IPAdapterStateDict = Dict[str, torch.Tensor]

def load_ip_adapter_tensors(ip_adapter_ckpt_path: pathlib.Path, device: str) -> IPAdapterStateDict:
    checkpoint = torch.load(str(ip_adapter_ckpt_path), map_location=device)
    ip_adapter_state_dict = {k: v.to(device) for k, v in checkpoint.items()}
    return ip_adapter_state_dict