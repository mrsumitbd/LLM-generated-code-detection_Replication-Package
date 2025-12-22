import torch

class VibeVoiceTokenizerEncoderOutput:
    """
    Output of VibeVoice tokenizer encoder, representing a Gaussian distribution with fixed variance.
    
    Args:
        mean (`torch.FloatTensor`): The mean parameters of the distribution.
        std (`float` or `torch.FloatTensor`): Fixed standard deviation value.
    """
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def sample(self, dist_type='fix'):
        if dist_type == 'fix':
            return self.mean + self.std * torch.randn_like(self.mean)
        else:
            raise ValueError("Invalid distribution type. Only 'fix' is supported.")

    def kl(self):
        return 0.5 * (self.std ** 2 + self.mean ** 2 - 1 - 2 * torch.log(self.std))

    def mode(self):
        return self.mean