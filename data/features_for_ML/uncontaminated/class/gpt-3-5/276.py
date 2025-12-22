class CogVAEDecoderStateDictConverter:

    def __init__(self):
        pass

    def from_diffusers(self, state_dict):
        converted_state_dict = {}
        for key, value in state_dict.items():
            new_key = key.replace('diffusers.', 'decoder.')
            converted_state_dict[new_key] = value
        return converted_state_dict

    def from_civitai(self, state_dict):
        converted_state_dict = {}
        for key, value in state_dict.items():
            new_key = key.replace('civitai.', 'decoder.')
            converted_state_dict[new_key] = value
        return converted_state_dict