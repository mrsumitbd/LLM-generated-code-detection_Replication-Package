import os
import json
import torch
from pathlib import Path


def load_state_dict_from_folder(file_path, torch_dtype=None):
    """
    Load a state dictionary from a folder containing model weights and metadata.
    
    Args:
        file_path: Path to the folder containing model files
        torch_dtype: Optional torch dtype to convert the loaded tensors to
        
    Returns:
        A dictionary containing the loaded state dict
    """
    file_path = Path(file_path)
    
    if not file_path.is_dir():
        raise ValueError(f"Path {file_path} is not a directory")
    
    state_dict = {}
    
    # Look for .pt, .pth, or .safetensors files
    pt_files = list(file_path.glob("*.pt")) + list(file_path.glob("*.pth"))
    
    if pt_files:
        # Load from PyTorch files
        for pt_file in pt_files:
            loaded = torch.load(pt_file, map_location="cpu")
            if isinstance(loaded, dict):
                state_dict.update(loaded)
            else:
                # If it's a single tensor, add it with a default key
                state_dict[pt_file.stem] = loaded
    else:
        # Try to load from safetensors if available
        try:
            from safetensors.torch import load_file
            safetensors_files = list(file_path.glob("*.safetensors"))
            if safetensors_files:
                for st_file in safetensors_files:
                    loaded = load_file(str(st_file))
                    state_dict.update(loaded)
        except ImportError:
            pass
    
    # If still no state dict, try loading from index files
    if not state_dict:
        index_file = file_path / "model.safetensors.index.json"
        if not index_file.exists():
            index_file = file_path / "pytorch_model.bin.index.json"
        
        if index_file.exists():
            with open(index_file, "r") as f:
                index_data = json.load(f)
            
            # Load weights from the files referenced in the index
            weight_map = index_data.get("weight_map", {})
            files_to_load = set(weight_map.values())
            
            for file_name in files_to_load:
                file_path_full = file_path / file_name
                if file_path_full.exists():
                    if file_name.endswith(".safetensors"):
                        try:
                            from safetensors.torch import load_file
                            loaded = load_file(str(file_path_full))
                            state_dict.update(loaded)
                        except ImportError:
                            pass
                    else:
                        loaded = torch.load(file_path_full, map_location="cpu")
                        if isinstance(loaded, dict):
                            state_dict.update(loaded)
    
    # Convert dtype if specified
    if torch_dtype is not None:
        for key in state_dict:
            if isinstance(state_dict[key], torch.Tensor):
                state_dict[key] = state_dict[key].to(torch_dtype)
    
    return state_dict