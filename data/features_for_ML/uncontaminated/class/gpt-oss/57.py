import cv2
import numpy as np
import torch
import random
from typing import Tuple


class EdgeControlModel:
    """
    A simple edge‑control model that applies Canny edge detection to each frame of a video.
    """

    # Mapping from string to (low, high) thresholds for Canny
    _threshold_map = {
        "low": (50, 150),
        "medium": (100, 200),
        "high": (150, 250),
    }

    def __init__(self, canny_threshold: str = "medium", use_random: bool = True):
        """
        Parameters
        ----------
        canny_threshold : str, optional
            One of "low", "medium", "high" to select the base Canny thresholds.
        use_random : bool, optional
            If True, randomize the thresholds within the selected range for each frame.
        """
        if canny_threshold not in self._threshold_map:
            raise ValueError(
                f"canny_threshold must be one of {list(self._threshold_map.keys())}"
            )
        self.base_low, self.base_high = self._threshold_map[canny_threshold]
        self.use_random = use_random

    def _load_frame(self, video_path: str) -> Tuple[np.ndarray, float, Tuple[int, int]]:
        """
        Load all frames from a video file.

        Returns
        -------
        frames : np.ndarray
            Array of shape (N, H, W, C) with dtype uint8.
        fps : float
            Frames per second of the input video.
        size : tuple
            (width, height) of the video frames.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video file {video_path}")

        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()

        if not frames:
            raise ValueError(f"No frames read from {video_path}")

        frames_np = np.stack(frames, axis=0)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        height, width = frames_np.shape[1:3]
        return frames_np, fps, (width, height)

    def __call__(self, input_video: str, output_video: str) -> None:
        """
        Process the input video and write the edge‑controlled output.

        Parameters
        ----------
        input_video : str
            Path to the input video file.
        output_video : str
            Path where the processed video will be saved.
        """
        frames_np, fps, size = self._load_frame(input_video)

        processed_frames = []
        for frame in frames_np:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if self.use_random:
                low = random.randint(self.base_low, self.base_high)
                high = random.randint(low, self.base_high)
            else:
                low, high = self.base_low, self.base_high

            edges = cv2.Canny(gray, low, high)
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            processed_frames.append(edges_colored)

        processed_np = np.stack(processed_frames, axis=0)
        processed_tensor = torch.from_numpy(processed_np).permute(0, 3, 1, 2).float() / 255.0
        self._save_output_video(processed_tensor, output_video, fps, size)

    def _save_output_video(
        self, frames: torch.Tensor, output_path: str, fps: float, size: Tuple[int, int]
    ) -> None:
        """
        Save a sequence of frames (torch.Tensor) to a video file.

        Parameters
        ----------
        frames : torch.Tensor
            Tensor of shape (N, C, H, W) with values in [0, 1].
        output_path : str
            Destination file path.
        fps : float
            Frames per second for the output video.
        size : tuple
            (width, height) of the video frames.
        """
        if frames.ndim != 4:
            raise ValueError("frames tensor must be 4D (N, C, H, W)")

        N, C, H, W = frames.shape
        if C != 3:
            raise ValueError("frames tensor must have 3 channels")

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, size)

        for i in range(N):
            frame = frames[i].permute(1, 2, 0).cpu().numpy()  # (H, W, C)
            frame = (frame * 255).astype(np.uint8)
            out.write(frame)

        out.release()