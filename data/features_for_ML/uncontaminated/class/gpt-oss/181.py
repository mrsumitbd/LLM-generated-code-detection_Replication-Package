import numpy as np

class FastBlendSmoother:
    def __init__(self):
        self.smoothed_frames = None
        self.window_size = None

    @staticmethod
    def from_model_manager(model_manager):
        # The model_manager is not used in this simplified implementation
        return FastBlendSmoother()

    def run(self, frames_guide, frames_style, batch_size, window_size, ebsynth_config):
        """
        Compute a simple temporal smoothing of the guide frames.
        The style frames are ignored in this simplified implementation.
        """
        self.window_size = window_size
        n_frames = len(frames_guide)
        smoothed = []
        for i in range(n_frames):
            start = max(0, i - window_size)
            end = min(n_frames, i + window_size + 1)
            window = frames_guide[start:end]
            # Ensure all frames in the window have the same shape
            window_arr = np.stack(window, axis=0)
            smoothed.append(np.mean(window_arr, axis=0))
        self.smoothed_frames = smoothed
        return smoothed

    def __call__(self, rendered_frames, original_frames=None, **kwargs):
        """
        Blend the rendered frames with the original frames if provided.
        If original_frames is None, return the rendered frames unchanged.
        """
        if original_frames is None:
            return rendered_frames

        blended = []
        for r, o in zip(rendered_frames, original_frames):
            # Simple average blending
            blended.append(0.5 * r + 0.5 * o)
        return blended