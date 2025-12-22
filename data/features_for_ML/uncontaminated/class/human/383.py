from typing import Dict, List, Optional, Tuple, Union
import torch
import torch.nn.functional as F

class VibeVoiceTokenizerEncoderOutput:
    """
    Output of VibeVoice tokenizer encoder, representing a Gaussian distribution with fixed variance.
    
    Args:
        mean (`torch.FloatTensor`): The mean parameters of the distribution.
        std (`float` or `torch.FloatTensor`): Fixed standard deviation value.
    """
    mean: torch.Tensor
    std: Optional[Union[float, torch.Tensor]] = None
    
    def sample(self, dist_type='fix'):
        """
        Sample from the distribution.
        
        Args:
            dist_type (`str`): Sampling method, either 'fix' or 'gaussian'.
                
        Returns:
            `torch.FloatTensor`: Sampled values.
            `torch.FloatTensor` (optional): Standard deviation used (only when dist_type='gaussian').
        """
        if dist_type == 'fix':
            x = self.mean + self.std * torch.randn_like(self.mean)
            return x, self.std
        elif dist_type == 'gaussian':
            batch_size = self.mean.size(0)
            value = self.std / 0.8
            std = torch.randn(batch_size, device=self.mean.device, dtype=self.mean.dtype) * value

            while std.dim() < self.mean.dim():
                std = std.unsqueeze(-1)

            x = self.mean + std * torch.randn_like(self.mean)
            return x, std
        else:
            return self.mean, self.std

    def kl(self):
        """Compute KL divergence between this distribution and a standard normal."""
        target = torch.zeros_like(self.mean)
        return F.mse_loss(self.mean, target, reduction='none')

    def mode(self):
        """Return the distribution mode (which is the mean for Gaussian)."""
        return self.mean