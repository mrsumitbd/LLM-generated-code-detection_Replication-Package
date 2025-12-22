import numpy as np
from dataclasses import dataclass
from typing import Any, Tuple


@dataclass
class AnisotropicDiffusionConfig:
    """
    Configuration for anisotropic diffusion.

    Attributes
    ----------
    num_iter : int
        Number of diffusion iterations.
    kappa : float
        Conduction coefficient (controls sensitivity to edges).
    lambda_ : float
        Integration constant (time step). Must be <= 0.25 for stability.
    option : int
        1 for Perona-Malik diffusion function 1,
        2 for Perona-Malik diffusion function 2.
    """
    num_iter: int = 10
    kappa: float = 30.0
    lambda_: float = 0.2
    option: int = 1


class AnisotropicDiffusion:
    """
    Applies Anisotropic Diffusion to images or video frames.
    """

    def __init__(self, config: AnisotropicDiffusionConfig) -> None:
        self.config = config
        if self.config.lambda_ > 0.25:
            raise ValueError("lambda_ must be <= 0.25 for stability.")
        if self.config.option not in (1, 2):
            raise ValueError("option must be 1 or 2.")

    def _diffuse(self, img: np.ndarray) -> np.ndarray:
        """Apply one diffusion iteration to a single channel image."""
        kappa = self.config.kappa
        lam = self.config.lambda_
        option = self.config.option

        # Compute gradients
        north = np.roll(img, -1, axis=0) - img
        south = np.roll(img, 1, axis=0) - img
        east = np.roll(img, -1, axis=1) - img
        west = np.roll(img, 1, axis=1) - img

        # Conduction coefficients
        if option == 1:
            cN = np.exp(-(north / kappa) ** 2)
            cS = np.exp(-(south / kappa) ** 2)
            cE = np.exp(-(east / kappa) ** 2)
            cW = np.exp(-(west / kappa) ** 2)
        else:  # option == 2
            cN = 1.0 / (1.0 + (north / kappa) ** 2)
            cS = 1.0 / (1.0 + (south / kappa) ** 2)
            cE = 1.0 / (1.0 + (east / kappa) ** 2)
            cW = 1.0 / (1.0 + (west / kappa) ** 2)

        # Update image
        img += lam * (
            cN * north + cS * south + cE * east + cW * west
        )
        return img

    def __call__(self, frames: np.ndarray) -> np.ndarray:
        """
        Apply anisotropic diffusion to the input frames.

        Parameters
        ----------
        frames : np.ndarray
            Input image or video frames. Expected shapes:
            - (H, W, C) for a single image
            - (N, H, W, C) for a batch of frames

        Returns
        -------
        np.ndarray
            Diffused frames with the same shape as the input.
        """
        if frames.ndim == 3:
            # Single image
            frames = frames[np.newaxis, ...]
            single = True
        elif frames.ndim == 4:
            single = False
        else:
            raise ValueError("Input must be 3D (H,W,C) or 4D (N,H,W,C).")

        out = np.empty_like(frames, dtype=np.float32)
        for i in range(frames.shape[0]):
            frame = frames[i].astype(np.float32)
            # Process each channel independently
            for c in range(frame.shape[2]):
                channel = frame[..., c]
                for _ in range(self.config.num_iter):
                    channel = self._diffuse(channel)
                out[i, ..., c] = channel

        if single:
            return out[0]
        return out