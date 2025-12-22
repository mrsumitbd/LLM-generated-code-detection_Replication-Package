class AnisotropicDiffusion:
    """
    Applies Anisotropic Diffusion to images or video frames.
    """

    def __init__(self, config: AnisotropicDiffusionConfig) -> None:
        self.config = config
        self.num_iterations = config.num_iterations
        self.kappa = config.kappa
        self.gamma = config.gamma
        self.option = config.option

    def __call__(self, frames: np.ndarray) -> np.ndarray:
        """
        Apply anisotropic diffusion to frames.
        
        Args:
            frames: Input frames of shape (H, W) or (T, H, W) or (T, H, W, C)
            
        Returns:
            Filtered frames with same shape as input
        """
        if frames.ndim == 2:
            return self._apply_diffusion_2d(frames)
        elif frames.ndim == 3:
            if frames.shape[0] < frames.shape[1]:  # Likely (T, H, W)
                return np.array([self._apply_diffusion_2d(frame) for frame in frames])
            else:  # Likely (H, W, C)
                return np.stack([self._apply_diffusion_2d(frames[:, :, c]) for c in range(frames.shape[2])], axis=2)
        elif frames.ndim == 4:  # (T, H, W, C)
            return np.array([[self._apply_diffusion_2d(frames[t, :, :, c]) for c in range(frames.shape[3])] for t in range(frames.shape[0])])
        else:
            raise ValueError(f"Unsupported frame shape: {frames.shape}")

    def _apply_diffusion_2d(self, frame: np.ndarray) -> np.ndarray:
        """
        Apply anisotropic diffusion to a 2D frame.
        
        Args:
            frame: 2D input frame
            
        Returns:
            Filtered 2D frame
        """
        output = frame.astype(np.float32).copy()
        
        for _ in range(self.num_iterations):
            output = self._diffusion_step(output)
        
        return np.clip(output, frame.min(), frame.max()).astype(frame.dtype)

    def _diffusion_step(self, frame: np.ndarray) -> np.ndarray:
        """
        Perform one step of anisotropic diffusion.
        
        Args:
            frame: Input frame
            
        Returns:
            Frame after one diffusion step
        """
        h, w = frame.shape
        output = frame.copy()
        
        # Compute gradients in all directions
        north = np.roll(frame, 1, axis=0) - frame
        south = np.roll(frame, -1, axis=0) - frame
        east = np.roll(frame, -1, axis=1) - frame
        west = np.roll(frame, 1, axis=1) - frame
        
        # Compute diffusion coefficients based on gradients
        if self.option == 1:
            # Exponential diffusion coefficient
            cn = np.exp(-(north / self.kappa) ** 2)
            cs = np.exp(-(south / self.kappa) ** 2)
            ce = np.exp(-(east / self.kappa) ** 2)
            cw = np.exp(-(west / self.kappa) ** 2)
        elif self.option == 2:
            # Reciprocal diffusion coefficient
            cn = 1.0 / (1.0 + (north / self.kappa) ** 2)
            cs = 1.0 / (1.0 + (south / self.kappa) ** 2)
            ce = 1.0 / (1.0 + (east / self.kappa) ** 2)
            cw = 1.0 / (1.0 + (west / self.kappa) ** 2)
        else:
            raise ValueError(f"Unknown diffusion option: {self.option}")
        
        # Update frame using diffusion equation
        output = frame + self.gamma * (
            cn * north + cs * south + ce * east + cw * west
        )
        
        return output