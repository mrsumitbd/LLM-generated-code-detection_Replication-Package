import torch

class GaussianNormalize:

    def input(self, input: torch.Tensor):
        mean = torch.mean(input)
        std = torch.std(input)
        self.mean = mean
        self.std = std
        return (input - mean) / std

    def output(self, output):
        return output * self.std + self.mean