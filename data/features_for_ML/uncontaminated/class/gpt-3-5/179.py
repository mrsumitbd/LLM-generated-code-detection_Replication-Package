from PIL import Image
import numpy as np

class DepthAnythingModel:

    def __init__(self):
        pass

    def predict_depth(self, image: Image.Image) -> Image.Image:
        pass

    def __call__(self, input_video: str, output_video: str = "depth.mp4") -> str:
        pass

    @staticmethod
    def save_depth(output: np.ndarray) -> Image.Image:
        pass

    @staticmethod
    def write_video(frames, output_path, fps=30):
        pass