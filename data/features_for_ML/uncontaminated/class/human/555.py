import numpy as np

class PostprocessingGuardrail:
    def postprocess(self, frames: np.ndarray) -> np.ndarray:
        raise NotImplementedError("Child classes must implement the postprocess method")