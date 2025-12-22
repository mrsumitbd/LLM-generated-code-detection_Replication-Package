import os
import torch

def load_state_dict_from_folder(file_path, torch_dtype=None):
    """
    Loads a PyTorch state dictionary from a folder.

    Args:
        file_path (str): The path to the folder containing the state dictionary files.
        torch_dtype (torch.dtype, optional): The data type to use for the loaded tensors. If not provided, the original data type will be used.

    Returns:
        dict: The loaded state dictionary.
    """
    state_dict = {}
    for filename in os.listdir(file_path):
        if filename.endswith(".pt") or filename.endswith(".pth"):
            tensor_name = os.path.splitext(filename)[0]
            tensor_path = os.path.join(file_path, filename)
            tensor = torch.load(tensor_path, map_location=torch.device('cpu'))
            if torch_dtype is not None:
                tensor = tensor.to(torch_dtype)
            state_dict[tensor_name] = tensor
    return state_dict