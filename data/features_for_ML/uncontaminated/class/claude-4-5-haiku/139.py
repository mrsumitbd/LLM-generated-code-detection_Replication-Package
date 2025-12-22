import torch

class GaussianNormalize:
    def __init__(self):
        self.mean = None
        self.std = None

    def input(self, input: torch.Tensor):
        if self.mean is None:
            self.mean = input.mean(dim=0)
            self.std = input.std(dim=0)
            self.std[self.std == 0] = 1.0
        return (input - self.mean) / self.std

    def output(self, output):
        if self.mean is None or self.std is None:
            return output
        return output * self.std + self.mean