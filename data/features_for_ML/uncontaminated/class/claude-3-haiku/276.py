class CogVAEDecoderStateDictConverter:
    def __init__(self):
        self.mapping = {
            "time_embed.0.weight": "time_embed.weight",
            "time_embed.0.bias": "time_embed.bias",
            "conv_in.weight": "conv_in.weight",
            "conv_in.bias": "conv_in.bias",
            "norm1.weight": "norm1.weight",
            "norm1.bias": "norm1.bias",
            "conv_out.weight": "conv_out.weight",
            "conv_out.bias": "conv_out.bias",
            "norm2.weight": "norm2.weight",
            "norm2.bias": "norm2.bias",
            "latent_conv.weight": "latent_conv.weight",
            "latent_conv.bias": "latent_conv.bias",
        }

    def from_diffusers(self, state_dict):
        new_state_dict = {}
        for key, value in state_dict.items():
            if key in self.mapping:
                new_state_dict[self.mapping[key]] = value
            else:
                new_state_dict[key] = value
        return new_state_dict

    def from_civitai(self, state_dict):
        new_state_dict = {}
        for key, value in state_dict.items():
            if key in self.mapping:
                new_state_dict[self.mapping[key]] = value
            else:
                new_state_dict[key] = value
        return new_state_dict