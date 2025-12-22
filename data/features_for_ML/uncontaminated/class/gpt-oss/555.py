import numpy as np

class PostprocessingGuardrail:
    """
    A simple guardrail that ensures the output frames are valid image tensors.
    It clips pixel values to the 0‑255 range and casts the array to uint8.
    """

    def postprocess(self, frames: np.ndarray) -> np.ndarray:
        """
        Clip the input frames to the valid pixel range [0, 255] and cast to uint8.

        Parameters
        ----------
        frames : np.ndarray
            The raw output from a model. Expected to be a numeric array
            with pixel values possibly outside the 0‑255 range.

        Returns
        -------
        np.ndarray
            The processed frames with values clipped to [0, 255] and dtype uint8.
        """
        # Ensure we work on a copy to avoid side‑effects
        processed = np.clip(frames, 0, 255)
        # Convert to unsigned 8‑bit integer if not already
        if processed.dtype != np.uint8:
            processed = processed.astype(np.uint8)
        return processed