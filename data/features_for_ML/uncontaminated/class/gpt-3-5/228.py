from typing import Tuple
import numpy as np

class GuidedFilterConfig:
    def __init__(self, radius: int, eps: float) -> None:
        self.radius = radius
        self.eps = eps

class GuidedFilter:

    def __init__(self, config: GuidedFilterConfig) -> None:
        self.radius = config.radius
        self.eps = config.eps

    def __call__(self, frames: np.ndarray) -> np.ndarray:
        return frames  # Placeholder implementation, replace with actual guided filter implementation

# Example usage:
config = GuidedFilterConfig(radius=3, eps=0.1)
guided_filter = GuidedFilter(config)
frames = np.random.rand(100, 100, 3)  # Example input frames
filtered_frames = guided_filter(frames)  # Apply guided filter to input frames
print(filtered_frames)