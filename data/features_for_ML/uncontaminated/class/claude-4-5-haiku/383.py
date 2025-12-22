import torch
import torch.nn.functional as F

class VibeVoiceTokenizerEncoderOutput:
    """
    Output of VibeVoice tokenizer encoder, representing a Gaussian distribution with fixed variance.
    
    Args:
        mean (`torch.FloatTensor`): The mean parameters of the distribution.
        std (`float` or `torch.FloatTensor`): Fixed standard deviation value.
    """

    def __init__(self, mean, std):
        self.mean = mean
        if isinstance(std, float):
            self.std = torch.tensor(std, dtype=mean.dtype, device=mean.device)
        else:
            self.std = std

    def sample(self, dist_type='fix'):
        """
        Sample from the Gaussian distribution.
        
        Args:
            dist_type (`str`): Type of distribution. If 'fix', uses fixed std. Otherwise uses learnable std.
        
        Returns:
            `torch.FloatTensor`: Sampled values from the distribution.
        """
        if dist_type == 'fix':
            std = self.std
        else:
            std = self.std
        
        epsilon = torch.randn_like(self.mean)
        sample = self.mean + std * epsilon
        return sample

    def kl(self):
        """
        Compute KL divergence between the distribution and standard normal N(0, 1).
        
        Returns:
            `torch.FloatTensor`: KL divergence value.
        """
        # KL(N(mean, std^2) || N(0, 1)) = 0.5 * sum(mean^2 + std^2 - 1 - log(std^2))
        var = self.std ** 2
        kl_loss = 0.5 * torch.sum(
            self.mean ** 2 + var - 1 - torch.log(var + 1e-10)
        )
        return kl_loss

    def mode(self):
        """
        Get the mode (mean) of the distribution.
        
        Returns:
            `torch.FloatTensor`: The mean of the distribution.
        """
        return self.mean