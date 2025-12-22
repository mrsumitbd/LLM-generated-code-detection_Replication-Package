import torch

class GaussianNormalize:
    def input(self, input: torch.Tensor):
        self.mean = torch.mean(input, tuple(range(1, input.dim())), keepdim=True)
        self.std = torch.std(input, tuple(range(1, input.dim())), keepdim=True)
        return (input - self.mean.detach()) / self.std.detach()

    def output(self, output):
        return self.mean.detach() + self.std.detach() * output