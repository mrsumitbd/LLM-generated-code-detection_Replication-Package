import torch
import torch.nn.functional as F

def add_fourier_features(inputs: torch.Tensor, start=6, stop=8, step=1):
    n = inputs.size(1)
    for freq in range(start, stop, step):
        inputs = torch.cat((inputs, torch.sin(freq * inputs), torch.cos(freq * inputs)), dim=1)
    return inputs