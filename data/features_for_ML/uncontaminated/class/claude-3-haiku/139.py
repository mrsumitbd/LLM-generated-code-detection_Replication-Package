import torch

class GaussianNormalize:
    def __init__(self, mean=0.0, std=1.0):
        self.mean = mean
        self.std = std

    def input(self, input: torch.Tensor):
        self.input_tensor = input
        self.normalized_input = (self.input_tensor - self.mean) / self.std
        return self.normalized_input

    def output(self, output):
        self.output_tensor = output
        self.denormalized_output = (self.output_tensor * self.std) + self.mean
        return self.denormalized_output