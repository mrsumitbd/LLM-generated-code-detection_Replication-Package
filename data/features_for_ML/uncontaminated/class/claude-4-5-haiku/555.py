import numpy as np
from typing import Optional

class PostprocessingGuardrail:
    """
    A guardrail for postprocessing operations on frame sequences.
    Ensures frames are valid and applies safety checks.
    """

    def __init__(self, 
                 min_value: float = 0.0,
                 max_value: float = 255.0,
                 dtype: Optional[np.dtype] = None):
        self.min_value = min_value
        self.max_value = max_value
        self.dtype = dtype or np.uint8

    def postprocess(self, frames: np.ndarray) -> np.ndarray:
        """
        Postprocess frames with safety guardrails.
        
        Args:
            frames: Input frame array of shape (batch, height, width, channels) or similar
            
        Returns:
            Postprocessed frames with applied guardrails
        """
        if frames is None or frames.size == 0:
            return frames
        
        # Clip values to valid range
        processed = np.clip(frames, self.min_value, self.max_value)
        
        # Convert to appropriate dtype
        if self.dtype in [np.uint8, np.uint16, np.uint32, np.uint64]:
            processed = np.round(processed).astype(self.dtype)
        else:
            processed = processed.astype(self.dtype)
        
        return processed