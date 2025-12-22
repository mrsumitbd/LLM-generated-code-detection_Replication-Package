class GuidedFilter:

    def __init__(self, config: GuidedFilterConfig) -> None:
        self.config = config
        self.radius = config.radius
        self.eps = config.eps

    def __call__(self, frames: np.ndarray) -> np.ndarray:
        """
        Apply guided filter to frames.
        
        Args:
            frames: Input frames of shape (H, W, C) or (H, W)
            
        Returns:
            Filtered frames of same shape as input
        """
        if frames.ndim == 2:
            return self._filter_single_channel(frames, frames)
        elif frames.ndim == 3:
            if frames.shape[2] == 1:
                frames = frames[:, :, 0]
                return self._filter_single_channel(frames, frames)[:, :, np.newaxis]
            else:
                result = np.zeros_like(frames)
                for c in range(frames.shape[2]):
                    result[:, :, c] = self._filter_single_channel(frames[:, :, c], frames[:, :, c])
                return result
        else:
            raise ValueError(f"Unsupported frame shape: {frames.shape}")

    def _filter_single_channel(self, I: np.ndarray, p: np.ndarray) -> np.ndarray:
        """
        Apply guided filter to a single channel.
        
        Args:
            I: Guidance image
            p: Input image to filter
            
        Returns:
            Filtered image
        """
        I = I.astype(np.float32)
        p = p.astype(np.float32)
        
        r = self.radius
        eps = self.eps
        
        H, W = I.shape
        
        # Compute local means
        mean_I = cv2.blur(I, (2*r+1, 2*r+1))
        mean_p = cv2.blur(p, (2*r+1, 2*r+1))
        
        # Compute local variances and covariances
        mean_II = cv2.blur(I * I, (2*r+1, 2*r+1))
        mean_Ip = cv2.blur(I * p, (2*r+1, 2*r+1))
        
        var_I = mean_II - mean_I * mean_I
        cov_Ip = mean_Ip - mean_I * mean_p
        
        # Compute filter coefficients
        a = cov_Ip / (var_I + eps)
        b = mean_p - a * mean_I
        
        # Compute output
        mean_a = cv2.blur(a, (2*r+1, 2*r+1))
        mean_b = cv2.blur(b, (2*r+1, 2*r+1))
        
        q = mean_a * I + mean_b
        
        return q