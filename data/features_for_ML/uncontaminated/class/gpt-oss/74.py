import os
import cv2
import mediapipe as mp
import numpy as np

class StableAnimatorSkeletonNode:
    """
    StableAnimator生成视频POSE骨架
    """

    def __init__(self):
        self.pose = mp.solutions.pose.Pose(static_image_mode=True,
                                           model_complexity=2,
                                           enable_segmentation=False,
                                           min_detection_confidence=0.5)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("STRING", {"default": "", "tooltip": "Path to an image file"}),
                "video": ("STRING", {"default": "", "tooltip": "Path to a video file"}),
                "frame": ("INT", {"default": 0, "tooltip": "Frame index to extract from video"}),
            }
        }

    def extraction(self, **kwargs):
        image_path = kwargs.get("image", "")
        video_path = kwargs.get("video", "")
        frame_idx = kwargs.get("frame", 0)

        if image_path and os.path.isfile(image_path):
            return self._extract_from_image(image_path)
        elif video_path and os.path.isfile(video_path):
            return self._extract_from_video(video_path, frame_idx)
        else:
            raise ValueError("Either a valid image path or video path must be provided.")

    def _extract_from_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Unable to read image: {image_path}")
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        return self._format_results(results)

    def _extract_from_video(self, video_path, frame_idx):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Unable to open video: {video_path}")
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if frame_idx < 0 or frame_idx >= total_frames:
            raise ValueError(f"Frame index {frame_idx} out of range (0-{total_frames-1})")
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            raise ValueError(f"Unable to read frame {frame_idx} from video.")
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        return self._format_results(results)

    def _format_results(self, results):
        if not results.pose_landmarks:
            return {"landmarks": []}
        landmarks = []
        for idx, lm in enumerate(results.pose_landmarks.landmark):
            landmarks.append({
                "index": idx,
                "x": lm.x,
                "y": lm.y,
                "z": lm.z,
                "visibility": lm.visibility
            })
        return {"landmarks": landmarks}