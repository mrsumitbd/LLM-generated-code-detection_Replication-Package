import cv2
import numpy as np
import torch
from typing import Tuple

class EdgeControlModel:
    def __init__(self, canny_threshold="medium", use_random=True):
        self.canny_threshold = canny_threshold
        self.use_random = use_random
        self.canny_thresholds = {"low": (100, 200), "medium": (150, 300), "high": (200, 400)}

    def _load_frame(self, video_path: str) -> np.ndarray:
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        cap.release()
        return frame

    def __call__(self, input_video, output_video):
        frames = []
        cap = cv2.VideoCapture(input_video)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            edge_frame = self._apply_edge_detection(frame)
            frames.append(torch.from_numpy(edge_frame))
        cap.release()
        self._save_output_video(torch.stack(frames), output_video)

    def _apply_edge_detection(self, frame: np.ndarray) -> np.ndarray:
        if self.canny_threshold == "random":
            low, high = self.canny_thresholds["low"] if self.use_random else self.canny_thresholds["high"]
        else:
            low, high = self.canny_thresholds[self.canny_threshold]
        return cv2.Canny(frame, low, high)

    def _save_output_video(self, frames: torch.Tensor, output_path: str) -> None:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 30.0, (frames[0].shape[1], frames[0].shape[0]))
        for frame in frames:
            out.write(frame.byte().numpy())
        out.release()