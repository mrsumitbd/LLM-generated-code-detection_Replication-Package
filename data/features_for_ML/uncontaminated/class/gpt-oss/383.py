import torch
import torch.nn.functional as F

class VibeVoiceTokenizerEncoderOutput:
    """
    Output of VibeVoice tokenizer encoder, representing a Gaussian distribution with fixed variance.

    Args:
        mean (torch.FloatTensor): The mean parameters of the distribution.
        std (float or torch.FloatTensor): Fixed standard deviation value.
    """

    def __init__(self, mean: torch.FloatTensor, std):
        self.mean = mean
        if isinstance(std, torch.Tensor):
            self.std = std
        else:
            self.std = torch.tensor(std, dtype=mean.dtype, device=mean.device)

    def sample(self, dist_type='fix'):
        """
        Sample from the Gaussian distribution.

        Args:
            dist_type (str): Currently only 'fix' is supported, which uses the fixed std.

        Returns:
            torch.FloatTensor: Sampled tensor.
        """
        if dist_type != 'fix':
            raise ValueError(f"Unsupported dist_type: {dist_type}")
        eps = torch.randn_like(self.mean)
        return self.mean + self.std * eps

    def kl(self):
        """
        Compute the KL divergence between this Gaussian and a standard normal N(0,1).

        Returns:
            torch.FloatTensor: KL divergence (scalar).
        """
        var = self.std ** 2
        # KL(N(mean,var) || N(0,1)) = 0.5 * (var + mean^2 - 1 - log(var))
        kl_per_dim = 0.5 * (var + self.mean ** 2 - 1 - torch.log(var))
        return kl_per_dim.sum()

    def mode(self):
        """
        Return the mode of the Gaussian distribution (which is the mean).

        Returns:
            torch.FloatTensor: Mode of the distribution.
        """
        return self.mean