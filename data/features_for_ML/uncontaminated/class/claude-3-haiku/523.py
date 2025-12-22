import numpy as np
from typing import Tuple

class AnisotropicDiffusionConfig:
    def __init__(self, num_iterations: int, time_step: float, kappa: float, sigma: float):
        self.num_iterations = num_iterations
        self.time_step = time_step
        self.kappa = kappa
        self.sigma = sigma

class AnisotropicDiffusion:
    """
    Applies Anisotropic Diffusion to images or video frames.
    """

    def __init__(self, config: AnisotropicDiffusionConfig) -> None:
        self.config = config

    def __call__(self, frames: np.ndarray) -> np.ndarray:
        num_frames, height, width, channels = frames.shape
        output_frames = np.zeros_like(frames)

        for frame_idx in range(num_frames):
            output_frames[frame_idx] = self.apply_anisotropic_diffusion(frames[frame_idx])

        return output_frames

    def apply_anisotropic_diffusion(self, frame: np.ndarray) -> np.ndarray:
        height, width, channels = frame.shape
        output_frame = frame.copy()

        for _ in range(self.config.num_iterations):
            dx, dy = self.compute_gradients(output_frame)
            g_x, g_y = self.compute_conductance(dx, dy)
            output_frame = self.update_frame(output_frame, g_x, g_y)

        return output_frame

    def compute_gradients(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        dx = np.gradient(frame, axis=1)
        dy = np.gradient(frame, axis=0)
        return dx, dy

    def compute_conductance(self, dx: np.ndarray, dy: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        g_x = np.exp(-(dx / self.config.sigma) ** 2 / self.config.kappa)
        g_y = np.exp(-(dy / self.config.sigma) ** 2 / self.config.kappa)
        return g_x, g_y

    def update_frame(self, frame: np.ndarray, g_x: np.ndarray, g_y: np.ndarray) -> np.ndarray:
        dx, dy = self.compute_gradients(frame)
        new_frame = frame + self.config.time_step * (
            g_x * dx + g_y * dy
        )
        return new_frame