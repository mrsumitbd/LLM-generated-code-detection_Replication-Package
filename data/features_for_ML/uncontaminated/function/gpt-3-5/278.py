def load_state_dict_from_folder(file_path, torch_dtype=None):
    import torch
    state_dict = torch.load(file_path, map_location='cpu')
    if torch_dtype is not None:
        for key in list(state_dict.keys()):
            state_dict[key] = state_dict[key].to(torch_dtype)
    return state_dict