
class CogVAEDecoderStateDictConverter:
    def __init__(self):
        pass


    def from_diffusers(self, state_dict):
        rename_dict = {
            "decoder.conv_in.conv.weight": "conv_in.weight",
            "decoder.conv_in.conv.bias": "conv_in.bias",
            "decoder.up_blocks.0.upsamplers.0.conv.weight": "blocks.6.conv.weight",
            "decoder.up_blocks.0.upsamplers.0.conv.bias": "blocks.6.conv.bias",
            "decoder.up_blocks.1.upsamplers.0.conv.weight": "blocks.11.conv.weight",
            "decoder.up_blocks.1.upsamplers.0.conv.bias": "blocks.11.conv.bias",
            "decoder.up_blocks.2.upsamplers.0.conv.weight": "blocks.16.conv.weight",
            "decoder.up_blocks.2.upsamplers.0.conv.bias": "blocks.16.conv.bias",
            "decoder.norm_out.norm_layer.weight": "norm_out.norm_layer.weight",
            "decoder.norm_out.norm_layer.bias": "norm_out.norm_layer.bias",
            "decoder.norm_out.conv_y.conv.weight": "norm_out.conv_y.weight",
            "decoder.norm_out.conv_y.conv.bias": "norm_out.conv_y.bias",
            "decoder.norm_out.conv_b.conv.weight": "norm_out.conv_b.weight",
            "decoder.norm_out.conv_b.conv.bias": "norm_out.conv_b.bias",
            "decoder.conv_out.conv.weight": "conv_out.weight",
            "decoder.conv_out.conv.bias": "conv_out.bias"
        }
        prefix_dict = {
            "decoder.mid_block.resnets.0.": "blocks.0.",
            "decoder.mid_block.resnets.1.": "blocks.1.",
            "decoder.up_blocks.0.resnets.0.": "blocks.2.",
            "decoder.up_blocks.0.resnets.1.": "blocks.3.",
            "decoder.up_blocks.0.resnets.2.": "blocks.4.",
            "decoder.up_blocks.0.resnets.3.": "blocks.5.",
            "decoder.up_blocks.1.resnets.0.": "blocks.7.",
            "decoder.up_blocks.1.resnets.1.": "blocks.8.",
            "decoder.up_blocks.1.resnets.2.": "blocks.9.",
            "decoder.up_blocks.1.resnets.3.": "blocks.10.",
            "decoder.up_blocks.2.resnets.0.": "blocks.12.",
            "decoder.up_blocks.2.resnets.1.": "blocks.13.",
            "decoder.up_blocks.2.resnets.2.": "blocks.14.",
            "decoder.up_blocks.2.resnets.3.": "blocks.15.",
            "decoder.up_blocks.3.resnets.0.": "blocks.17.",
            "decoder.up_blocks.3.resnets.1.": "blocks.18.",
            "decoder.up_blocks.3.resnets.2.": "blocks.19.",
            "decoder.up_blocks.3.resnets.3.": "blocks.20.",
        }
        suffix_dict = {
            "norm1.norm_layer.weight": "norm1.norm_layer.weight",
            "norm1.norm_layer.bias": "norm1.norm_layer.bias",
            "norm1.conv_y.conv.weight": "norm1.conv_y.weight",
            "norm1.conv_y.conv.bias": "norm1.conv_y.bias",
            "norm1.conv_b.conv.weight": "norm1.conv_b.weight",
            "norm1.conv_b.conv.bias": "norm1.conv_b.bias",
            "norm2.norm_layer.weight": "norm2.norm_layer.weight",
            "norm2.norm_layer.bias": "norm2.norm_layer.bias",
            "norm2.conv_y.conv.weight": "norm2.conv_y.weight",
            "norm2.conv_y.conv.bias": "norm2.conv_y.bias",
            "norm2.conv_b.conv.weight": "norm2.conv_b.weight",
            "norm2.conv_b.conv.bias": "norm2.conv_b.bias",
            "conv1.conv.weight": "conv1.weight",
            "conv1.conv.bias": "conv1.bias",
            "conv2.conv.weight": "conv2.weight",
            "conv2.conv.bias": "conv2.bias",
            "conv_shortcut.weight": "conv_shortcut.weight",
            "conv_shortcut.bias": "conv_shortcut.bias",
        }
        state_dict_ = {}
        for name, param in state_dict.items():
            if name in rename_dict:
                state_dict_[rename_dict[name]] = param
            else:
                for prefix in prefix_dict:
                    if name.startswith(prefix):
                        suffix = name[len(prefix):]
                        state_dict_[prefix_dict[prefix] + suffix_dict[suffix]] = param
        return state_dict_
    

    def from_civitai(self, state_dict):
        return self.from_diffusers(state_dict)