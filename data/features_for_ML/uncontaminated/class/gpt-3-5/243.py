import torch

class SD3TextEncoder1StateDictConverter:

    def __init__(self):
        pass

    def from_diffusers(self, state_dict):
        new_state_dict = {}
        for key, value in state_dict.items():
            if key.startswith('encoder.'):
                new_key = key.replace('encoder.', 'encoder.layers.0.')
                new_state_dict[new_key] = value
        return new_state_dict

    def from_civitai(self, state_dict):
        new_state_dict = {}
        for key, value in state_dict.items():
            if key.startswith('model.encoder.'):
                new_key = key.replace('model.encoder.', 'model.encoder.layers.0.')
                new_state_dict[new_key] = value
        return new_state_dict