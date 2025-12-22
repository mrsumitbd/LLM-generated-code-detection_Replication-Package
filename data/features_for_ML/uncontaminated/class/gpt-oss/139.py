import torch

class GaussianNormalize:
    def __init__(self):
        self.input_mean = None
        self.input_std = None
        self.output_mean = None
        self.output_std = None

    def input(self, input: torch.Tensor):
        """
        Normalizes the input tensor to zero mean and unit variance.
        Stores the mean and std for later use.
        """
        self.input_mean = input.mean()
        self.input_std = input.std(unbiased=False)
        if self.input_std == 0:
            self.input_std = torch.tensor(1.0, device=input.device, dtype=input.dtype)
        return (input - self.input_mean) / self.input_std

    def output(self, output):
        """
        Normalizes the output tensor to zero mean and unit variance.
        If mean/std have not been set yet, they are computed from the provided output.
        """
        if not isinstance(output, torch.Tensor):
            raise TypeError("output must be a torch.Tensor")

        if self.output_mean is None or self.output_std is None:
            self.output_mean = output.mean()
            self.output_std = output.std(unbiased=False)
            if self.output_std == 0:
                self.output_std = torch.tensor(1.0, device=output.device, dtype=output.dtype)

        return (output - self.output_mean) / self.output_std