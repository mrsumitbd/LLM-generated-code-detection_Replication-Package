import torch

class VibeVoiceTokenizerEncoderOutput:
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def sample(self, dist_type='fix'):
        if dist_type == 'fix':
            return self.mean + self.std * torch.randn_like(self.mean)
        else:
            raise ValueError("Invalid distribution type. Use 'fix' for fixed standard deviation.")

    def kl(self):
        return 0.5 * torch.sum(torch.pow(self.mean, 2) + torch.pow(self.std, 2) - torch.log(torch.pow(self.std, 2)) - 1)

    def mode(self):
        return self.mean