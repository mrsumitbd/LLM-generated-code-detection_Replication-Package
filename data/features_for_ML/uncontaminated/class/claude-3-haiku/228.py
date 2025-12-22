import numpy as np

class GuidedFilter:
    def __init__(self, config: GuidedFilterConfig) -> None:
        self.radius = config.radius
        self.epsilon = config.epsilon

    def __call__(self, frames: np.ndarray) -> np.ndarray:
        batch_size, height, width, channels = frames.shape
        filtered_frames = np.zeros_like(frames)

        for i in range(batch_size):
            filtered_frames[i] = self.filter_image(frames[i])

        return filtered_frames

    def filter_image(self, frame: np.ndarray) -> np.ndarray:
        height, width, channels = frame.shape
        mean_I = self.boxfilter(frame, self.radius)
        mean_p = self.boxfilter(frame, self.radius)
        corr_I = self.boxfilter(frame * frame, self.radius)
        corr_Ip = self.boxfilter(frame * frame, self.radius)

        var_I = corr_I - mean_I * mean_I
        cov_Ip = corr_Ip - mean_I * mean_p

        a = cov_Ip / (var_I + self.epsilon)
        b = mean_p - a * mean_I

        mean_a = self.boxfilter(a, self.radius)
        mean_b = self.boxfilter(b, self.radius)

        return mean_a * frame + mean_b

    def boxfilter(self, x: np.ndarray, r: int) -> np.ndarray:
        height, width, channels = x.shape
        s = np.zeros((height + 1, width + 1, channels))
        s[:, :, :] = np.cumsum(np.cumsum(x, axis=0), axis=1)
        return (s[r:, r:, :] - s[:-r, r:, :] - s[r:, :-r, :] + s[:-r, :-r, :]) / ((2 * r + 1) ** 2)