import torch
import pathlib
from typing import Dict

def load_ip_adapter_tensors(ip_adapter_ckpt_path: pathlib.Path, device: str) -> Dict[str, torch.Tensor]:
    ip_adapter_state_dict = torch.load(ip_adapter_ckpt_path, map_location=device)
    return ip_adapter_state_dict