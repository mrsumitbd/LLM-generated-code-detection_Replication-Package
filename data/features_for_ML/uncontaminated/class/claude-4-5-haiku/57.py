import cv2
import numpy as np
import torch
from pathlib import Path


class EdgeControlModel:

    def __init__(self, canny_threshold="medium", use_random=True):
        self.canny_threshold = canny_threshold
        self.use_random = use_random
        
        # Set canny thresholds based on parameter
        if canny_threshold == "low":
            self.canny_low = 50
            self.canny_high = 150
        elif canny_threshold == "medium":
            self.canny_low = 100
            self.canny_high = 200
        elif canny_threshold == "high":
            self.canny_low = 150
            self.canny_high = 250
        else:
            self.canny_low = 100
            self.canny_high = 200

    def _load_frame(self, video_path: str) -> np.ndarray:
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        
        cap.release()
        return np.array(frames)

    def __call__(self, input_video, output_video):
        # Load frames from input video
        frames = self._load_frame(input_video)
        
        # Process frames to extract edges
        edge_frames = []
        for frame in frames:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Canny edge detection
            edges = cv2.Canny(gray, self.canny_low, self.canny_high)
            
            # Convert back to 3 channels for consistency
            edge_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            edge_frames.append(edge_frame)
        
        # Convert to tensor
        edge_tensor = torch.from_numpy(np.array(edge_frames)).float()
        
        # Save output video
        self._save_output_video(edge_tensor, output_video)

    def _save_output_video(self, frames: torch.Tensor, output_path: str) -> None:
        # Convert tensor to numpy array
        frames_np = frames.cpu().numpy().astype(np.uint8)
        
        # Get video properties
        num_frames, height, width, channels = frames_np.shape
        
        # Define codec and create VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = 30  # Default fps
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Write frames
        for frame in frames_np:
            # Convert RGB to BGR if needed
            if channels == 3:
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            else:
                frame_bgr = frame
            out.write(frame_bgr)
        
        out.release()