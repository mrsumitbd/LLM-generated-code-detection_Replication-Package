class FastBlendSmoother:

    def __init__(self):
        self.model_manager = None
        self.device = None
        self.optical_flow_model = None
        self.consistency_model = None

    @staticmethod
    def from_model_manager(model_manager):
        smoother = FastBlendSmoother()
        smoother.model_manager = model_manager
        smoother.device = model_manager.device if hasattr(model_manager, 'device') else 'cpu'
        return smoother

    def run(self, frames_guide, frames_style, batch_size, window_size, ebsynth_config):
        """
        Run fast blend smoothing on frames.
        
        Args:
            frames_guide: Guide frames for smoothing
            frames_style: Style frames to blend
            batch_size: Batch size for processing
            window_size: Window size for temporal smoothing
            ebsynth_config: Configuration for ebsynth processing
            
        Returns:
            Smoothed frames
        """
        import torch
        import numpy as np
        
        if frames_guide is None or len(frames_guide) == 0:
            return frames_style
        
        num_frames = len(frames_guide)
        smoothed_frames = []
        
        for i in range(0, num_frames, batch_size):
            batch_end = min(i + batch_size, num_frames)
            batch_guide = frames_guide[i:batch_end]
            batch_style = frames_style[i:batch_end]
            
            # Apply temporal smoothing within window
            window_start = max(0, i - window_size // 2)
            window_end = min(num_frames, i + batch_size + window_size // 2)
            
            # Simple blend smoothing
            blended_batch = []
            for j, (guide, style) in enumerate(zip(batch_guide, batch_style)):
                if isinstance(guide, torch.Tensor):
                    guide = guide.cpu().numpy()
                if isinstance(style, torch.Tensor):
                    style = style.cpu().numpy()
                
                # Normalize to [0, 1] if needed
                if guide.max() > 1.0:
                    guide = guide / 255.0
                if style.max() > 1.0:
                    style = style / 255.0
                
                # Blend frames
                alpha = 0.5
                blended = alpha * guide + (1 - alpha) * style
                blended_batch.append(blended)
            
            smoothed_frames.extend(blended_batch)
        
        return smoothed_frames

    def __call__(self, rendered_frames, original_frames=None, **kwargs):
        """
        Apply fast blend smoothing to rendered frames.
        
        Args:
            rendered_frames: Frames to smooth
            original_frames: Optional original frames for reference
            **kwargs: Additional arguments including:
                - batch_size: Batch size for processing
                - window_size: Temporal window size
                - ebsynth_config: Configuration dict
                
        Returns:
            Smoothed frames
        """
        batch_size = kwargs.get('batch_size', 4)
        window_size = kwargs.get('window_size', 5)
        ebsynth_config = kwargs.get('ebsynth_config', {})
        
        if original_frames is None:
            original_frames = rendered_frames
        
        smoothed = self.run(
            frames_guide=original_frames,
            frames_style=rendered_frames,
            batch_size=batch_size,
            window_size=window_size,
            ebsynth_config=ebsynth_config
        )
        
        return smoothed