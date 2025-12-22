import cv2
import numpy as np
from PIL import Image
import torch
from transformers import pipeline
import os

class DepthAnythingModel:

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = pipeline(
            task="depth-estimation",
            model="LiheYoung/depth-anything-small-hf",
            device=0 if self.device == "cuda" else -1
        )

    def predict_depth(self, image: Image.Image) -> Image.Image:
        depth = self.pipe(image)["depth"]
        return depth

    def __call__(self, input_video: str, output_video: str = "depth.mp4") -> str:
        cap = cv2.VideoCapture(input_video)
        
        if not cap.isOpened():
            raise ValueError(f"Cannot open video file: {input_video}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        frames = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            depth_map = self.predict_depth(pil_image)
            depth_image = self.save_depth(np.array(depth_map))
            
            frames.append(np.array(depth_image))
        
        cap.release()
        
        self.write_video(frames, output_video, fps)
        
        return output_video

    @staticmethod
    def save_depth(output: np.ndarray) -> Image.Image:
        output = np.array(output)
        
        if output.ndim == 3:
            output = output.squeeze()
        
        output_normalized = ((output - output.min()) / (output.max() - output.min()) * 255).astype(np.uint8)
        
        depth_colored = cv2.applyColorMap(output_normalized, cv2.COLORMAP_TURBO)
        depth_colored_rgb = cv2.cvtColor(depth_colored, cv2.COLOR_BGR2RGB)
        
        return Image.fromarray(depth_colored_rgb)

    @staticmethod
    def write_video(frames, output_path, fps=30):
        if len(frames) == 0:
            raise ValueError("No frames to write")
        
        frame_height, frame_width = frames[0].shape[:2]
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        
        for frame in frames:
            if frame.ndim == 3 and frame.shape[2] == 3:
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            else:
                frame_bgr = frame
            
            out.write(frame_bgr)
        
        out.release()