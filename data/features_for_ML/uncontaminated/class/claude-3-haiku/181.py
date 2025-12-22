import numpy as np
from ebsynth import EBSynthConfig, EBSynthBlender

class FastBlendSmoother:
    def __init__(self):
        self.blender = None

    @staticmethod
    def from_model_manager(model_manager):
        smoother = FastBlendSmoother()
        smoother.blender = EBSynthBlender(model_manager)
        return smoother

    def run(self, frames_guide, frames_style, batch_size, window_size, ebsynth_config):
        config = EBSynthConfig(batch_size=batch_size, window_size=window_size, **ebsynth_config)
        self.blender.blend(frames_guide, frames_style, config)

    def __call__(self, rendered_frames, original_frames=None, **kwargs):
        if original_frames is None:
            return self.blender.blend_frames(rendered_frames)
        else:
            return self.blender.blend_frames(rendered_frames, original_frames)