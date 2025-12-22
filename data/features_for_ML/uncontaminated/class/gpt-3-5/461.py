import torch

class SDUNetStateDictConverter:

    def __init__(self):
        pass

    def from_diffusers(self, state_dict):
        new_state_dict = {}
        for key, value in state_dict.items():
            new_key = key.replace('module.', '')  # Remove 'module.' prefix if present
            new_state_dict[new_key] = value
        return new_state_dict

    def from_civitai(self, state_dict):
        new_state_dict = {}
        for key, value in state_dict.items():
            new_key = 'model.' + key  # Add 'model.' prefix to keys
            new_state_dict[new_key] = value
        return new_state_dict