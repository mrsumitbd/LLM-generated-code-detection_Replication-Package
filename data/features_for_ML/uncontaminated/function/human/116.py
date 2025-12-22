import pathlib
import safetensors
import safetensors.torch
import torch

def load_ip_adapter_tensors(ip_adapter_ckpt_path: pathlib.Path, device: str) -> IPAdapterStateDict:
    state_dict: IPAdapterStateDict = {"ip_adapter": {}, "image_proj": {}}

    if ip_adapter_ckpt_path.suffix == ".safetensors":
        model = safetensors.torch.load_file(ip_adapter_ckpt_path, device=device)
        for key in model.keys():
            if key.startswith("image_proj."):
                state_dict["image_proj"][key.replace("image_proj.", "")] = model[key]
            elif key.startswith("ip_adapter."):
                state_dict["ip_adapter"][key.replace("ip_adapter.", "")] = model[key]
            else:
                raise RuntimeError(f"Encountered unexpected IP Adapter state dict key: '{key}'.")
    else:
        ip_adapter_diffusers_checkpoint_path = ip_adapter_ckpt_path / "ip_adapter.bin"
        state_dict = torch.load(ip_adapter_diffusers_checkpoint_path, map_location="cpu")

    return state_dict