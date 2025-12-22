import cv2
import numpy as np
import torch

class EdgeControlModel:

    def __init__(self, canny_threshold="medium", use_random=True):
        self.canny_threshold = canny_threshold
        self.use_random = use_random

    def _load_frame(self, video_path: str) -> np.ndarray:
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        cap.release()
        return frame

    def __call__(self, input_video, output_video):
        frame = self._load_frame(input_video)
        edges = cv2.Canny(frame, 100, 200)
        self._save_output_video(torch.Tensor(edges), output_video)

    def _save_output_video(self, frames: torch.Tensor, output_path: str) -> None:
        frames = frames.numpy().astype(np.uint8)
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frames.shape[1], frames.shape[0]))
        for frame in frames:
            out.write(frame)
        out.release()