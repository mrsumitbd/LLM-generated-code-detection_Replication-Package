class SDUNetStateDictConverter:
    def __init__(self):
        self.mapping = {
            "model.0.weight": "conv1.weight",
            "model.0.bias": "conv1.bias",
            "model.2.weight": "conv2.weight",
            "model.2.bias": "conv2.bias",
            "model.4.weight": "conv3.weight",
            "model.4.bias": "conv3.bias",
            "model.6.weight": "conv4.weight",
            "model.6.bias": "conv4.bias",
            "model.8.weight": "conv5.weight",
            "model.8.bias": "conv5.bias",
            "model.10.weight": "conv6.weight",
            "model.10.bias": "conv6.bias",
            "model.12.weight": "conv7.weight",
            "model.12.bias": "conv7.bias",
            "model.14.weight": "conv8.weight",
            "model.14.bias": "conv8.bias",
            "model.16.weight": "conv9.weight",
            "model.16.bias": "conv9.bias",
            "model.18.weight": "conv10.weight",
            "model.18.bias": "conv10.bias",
            "model.20.weight": "conv11.weight",
            "model.20.bias": "conv11.bias",
            "model.22.weight": "conv12.weight",
            "model.22.bias": "conv12.bias",
            "model.24.weight": "conv13.weight",
            "model.24.bias": "conv13.bias",
            "model.26.weight": "conv14.weight",
            "model.26.bias": "conv14.bias",
            "model.28.weight": "conv15.weight",
            "model.28.bias": "conv15.bias",
            "model.30.weight": "conv16.weight",
            "model.30.bias": "conv16.bias",
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