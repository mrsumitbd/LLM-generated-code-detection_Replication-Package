import numpy as np
from dataclasses import dataclass
from typing import Optional

try:
    from scipy.ndimage import uniform_filter
except ImportError:
    raise ImportError("scipy is required for GuidedFilter implementation")

@dataclass
class GuidedFilterConfig:
    radius: int = 5          # window radius
    eps: float = 1e-6        # regularization parameter
    guidance: Optional[np.ndarray] = None  # optional guidance image


class GuidedFilter:
    def __init__(self, config: GuidedFilterConfig) -> None:
        self.radius = config.radius
        self.eps = config.eps
        self.guidance = config.guidance

    def _filter_single(self, I: np.ndarray, p: np.ndarray) -> np.ndarray:
        """
        Apply guided filter to a single image.
        I: guidance image (H, W, C) or (H, W)
        p: filtering input (H, W, C) or (H, W)
        """
        # Ensure 3D arrays
        if I.ndim == 2:
            I = I[:, :, None]
        if p.ndim == 2:
            p = p[:, :, None]

        H, W, C = I.shape
        win_size = 2 * self.radius + 1

        # Compute means
        mean_I = uniform_filter(I, size=win_size, mode='reflect')
        mean_p = uniform_filter(p, size=win_size, mode='reflect')

        # Compute correlations
        corr_I = uniform_filter(I * I, size=win_size, mode='reflect')
        corr_Ip = uniform_filter(I * p, size=win_size, mode='reflect')

        # Variance and covariance
        var_I = corr_I - mean_I * mean_I
        cov_Ip = corr_Ip - mean_I * mean_p

        # Linear coefficients
        a = cov_Ip / (var_I + self.eps)
        b = mean_p - a * mean_I

        # Mean of coefficients
        mean_a = uniform_filter(a, size=win_size, mode='reflect')
        mean_b = uniform_filter(b, size=win_size, mode='reflect')

        # Output
        q = mean_a * I + mean_b
        if q.shape[2] == 1:
            q = q[:, :, 0]
        return q

    def __call__(self, frames: np.ndarray) -> np.ndarray:
        """
        Apply guided filter to input frames.
        frames: (H, W, C) or (N, H, W, C)
        """
        if frames.ndim == 3:
            # Single image
            I = self.guidance if self.guidance is not None else frames
            return self._filter_single(I, frames)
        elif frames.ndim == 4:
            # Batch of images
            N, H, W, C = frames.shape
            out = np.empty_like(frames)
            for i in range(N):
                I = self.guidance[i] if self.guidance is not None else frames[i]
                out[i] = self._filter_single(I, frames[i])
            return out
        else:
            raise ValueError("Unsupported input shape for GuidedFilter")