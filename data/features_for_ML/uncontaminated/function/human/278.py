import os

def load_state_dict_from_folder(file_path, torch_dtype=None):
    state_dict = {}
    for file_name in os.listdir(file_path):
        if "." in file_name and file_name.split(".")[-1] in ["safetensors", "bin", "ckpt", "pth", "pt"]:
            state_dict.update(load_state_dict(os.path.join(file_path, file_name), torch_dtype=torch_dtype))
    return state_dict