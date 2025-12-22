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

class GuidedFilter:
    def __init__(self, config: GuidedFilterConfig) -> None:
        self.use_random = config.use_random
        self.config = config

    def __call__(self, frames: np.ndarray) -> np.ndarray:
        if self.use_random:
            radius = np.random.randint(self.config.radius_min, self.config.radius_max + 1)
            eps = np.random.uniform(self.config.eps_min, self.config.eps_max)
            scale = np.random.randint(self.config.scale_min, self.config.scale_max + 1)
        else:
            radius = self.config.radius
            eps = self.config.eps
            scale = self.config.scale
        return apply_guided_filter(frames, radius, eps, scale)