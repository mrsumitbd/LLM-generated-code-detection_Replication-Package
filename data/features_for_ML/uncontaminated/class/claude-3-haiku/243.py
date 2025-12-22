class SD3TextEncoder1StateDictConverter:
    def __init__(self):
        self.text_encoder_key = "cond_stage_model.transformer.text_model."
        self.text_encoder_prefix = "text_encoder."

    def from_diffusers(self, state_dict):
        new_state_dict = {}
        for key, value in state_dict.items():
            if key.startswith(self.text_encoder_key):
                new_key = self.text_encoder_prefix + key[len(self.text_encoder_key):]
                new_state_dict[new_key] = value
        return new_state_dict

    def from_civitai(self, state_dict):
        new_state_dict = {}
        for key, value in state_dict.items():
            if key.startswith(self.text_encoder_prefix):
                new_state_dict[key] = value
        return new_state_dict