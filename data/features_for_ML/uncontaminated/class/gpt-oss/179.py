import os
import cv2
import numpy as np
from PIL import Image
from typing import List, Union


class DepthAnythingModel:
    """
    A lightweight depth estimation wrapper that can process single images or entire videos.
    The depth estimation is a simple gradient‑based proxy (not a real model) for demonstration.
    """

    def __init__(self):
        # No heavy model loading; placeholder for future integration
        pass

    def predict_depth(self, image: Image.Image) -> Image.Image:
        """
        Estimate a depth map from an RGB image.
        For demonstration, we use the magnitude of the image gradient as a proxy for depth.
        """
        # Convert to numpy array
        img_np = np.array(image.convert("RGB")).astype(np.float32) / 255.0
        # Compute gradients
        gx = cv2.Sobel(img_np, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(img_np, cv2.CV_32F, 0, 1, ksize=3)
        # Gradient magnitude
        depth = np.sqrt(gx ** 2 + gy ** 2)
        # Normalize to 0-255
        depth_norm = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
        depth_uint8 = depth_norm.astype(np.uint8)
        return Image.fromarray(depth_uint8)

    def __call__(self, input_video: str, output_video: str = "depth.mp4") -> str:
        """
        Process an input video frame‑by‑frame, compute depth maps, and write a new video.
        """
        if not os.path.isfile(input_video):
            raise FileNotFoundError(f"Input video not found: {input_video}")

        cap = cv2.VideoCapture(input_video)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video: {input_video}")

        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Prepare output writer
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height), isColor=False)

        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert BGR to RGB PIL image
            pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            depth_img = self.predict_depth(pil_img)
            depth_np = np.array(depth_img)

            # Write depth frame (single channel)
            out.write(depth_np)

            frame_idx += 1

        cap.release()
        out.release()
        return output_video

    @staticmethod
    def save_depth(output: np.ndarray) -> Image.Image:
        """
        Convert a depth array to a PIL Image.
        """
        if output.ndim == 3 and output.shape[2] == 3:
            # If RGB, convert to grayscale
            output = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
        depth_norm = cv2.normalize(output, None, 0, 255, cv2.NORM_MINMAX)
        depth_uint8 = depth_norm.astype(np.uint8)
        return Image.fromarray(depth_uint8)

    @staticmethod
    def write_video(frames: List[Union[Image.Image, np.ndarray]],
                    output_path: str,
                    fps: float = 30.0):
        """
        Write a list of frames to a video file.
        Each frame can be a PIL Image or a numpy array (BGR or RGB).
        """
        if not frames:
            raise ValueError("No frames provided for video writing.")

        # Determine frame size from first frame
        first_frame = frames[0]
        if isinstance(first_frame, Image.Image):
            frame_np = np.array(first_frame)
        else:
            frame_np = first_frame
        height, width = frame_np.shape[:2]

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)

        for idx, frame in enumerate(frames):
            if isinstance(frame, Image.Image):
                frame_np = np.array(frame)
            else:
                frame_np = frame

            # Ensure frame is in BGR format for OpenCV
            if frame_np.ndim == 2:  # grayscale
                frame_bgr = cv2.cvtColor(frame_np, cv2.COLOR_GRAY2BGR)
            elif frame_np.shape[2] == 3:
                # Assume RGB, convert to BGR
                frame_bgr = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)
            else:
                raise ValueError(f"Unsupported frame shape at index {idx}: {frame_np.shape}")

            out.write(frame_bgr)

        out.release()