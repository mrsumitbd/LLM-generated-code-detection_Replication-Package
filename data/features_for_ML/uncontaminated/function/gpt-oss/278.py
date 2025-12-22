import os
import torch

def load_state_dict_from_folder(file_path, torch_dtype=None):
    """
    Load a PyTorch state_dict from a folder or a single file.

    Parameters
    ----------
    file_path : str
        Path to a folder containing a single state_dict file (e.g., *.bin, *.pt, *.pth)
        or a direct path to a state_dict file.
    torch_dtype : torch.dtype, optional
        If provided, cast all tensors in the state_dict to this dtype.

    Returns
    -------
    dict
        The loaded state_dict.
    """
    # Resolve the actual file to load
    if os.path.isdir(file_path):
        # Find the first file with a common state_dict extension
        candidates = []
        for ext in (".bin", ".pt", ".pth"):
            for fname in os.listdir(file_path):
                if fname.endswith(ext):
                    candidates.append(os.path.join(file_path, fname))
        if not candidates:
            raise FileNotFoundError(
                f"No state_dict file found in directory '{file_path}'. "
                f"Expected one of: .bin, .pt, .pth"
            )
        # Prefer .bin over .pt/.pth if multiple found
        candidates.sort(key=lambda f: (not f.endswith(".bin"), f))
        state_dict_path = candidates[0]
    else:
        # Assume file_path is a file
        state_dict_path = file_path

    # Load the state_dict
    state_dict = torch.load(state_dict_path, map_location="cpu")

    # Ensure we have a dict
    if not isinstance(state_dict, dict):
        raise ValueError(
            f"Loaded object from '{state_dict_path}' is not a dict. "
            f"Got type {type(state_dict)}."
        )

    # Optionally cast tensors to the requested dtype
    if torch_dtype is not None:
        for k, v in state_dict.items():
            if isinstance(v, torch.Tensor):
                state_dict[k] = v.to(dtype=torch_dtype)

    return state_dict