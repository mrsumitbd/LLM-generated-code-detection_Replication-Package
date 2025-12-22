import numpy as np

class PostprocessingGuardrail:
    def __init__(self, min_value: float = 0.0, max_value: float = 1.0):
        self.min_value = min_value
        self.max_value = max_value

    def postprocess(self, frames: np.ndarray) -> np.ndarray:
        processed_frames = np.clip(frames, self.min_value, self.max_value)
        return processed_frames