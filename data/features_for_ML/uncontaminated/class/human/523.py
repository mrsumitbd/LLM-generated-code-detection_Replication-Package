import numpy as np
from cosmos_transfer1.diffusion.config.transfer.blurs import (
    AnisotropicDiffusionConfig,
    BilateralFilterConfig,
    BlurAugmentorConfig,
    GaussianBlurConfig,
    GuidedFilterConfig,
    LaplacianOfGaussianConfig,
    MedianBlurConfig,
)

class AnisotropicDiffusion:
    """
    Applies Anisotropic Diffusion to images or video frames.
    """

    def __init__(self, config: AnisotropicDiffusionConfig) -> None:
        self.use_random = config.use_random
        self.config = config

    def __call__(self, frames: np.ndarray) -> np.ndarray:
        if self.use_random:
            alpha = np.random.uniform(self.config.alpha_min, self.config.alpha_max)
            K = np.random.uniform(self.config.K_min, self.config.K_max)
            niters = np.random.randint(self.config.niters_min, self.config.niters_max + 1)
        else:
            alpha = self.config.alpha
            K = self.config.K
            niters = self.config.niters
        return apply_anisotropic_diffusion(frames, alpha, K, niters)