def fetch_video(
    ele: dict, return_video_sample_fps: bool = False
) -> torch.Tensor | list[Image.Image]:
    """
    Fetch video frames from a video element.
    
    Args:
        ele: Dictionary containing video information with keys like 'video_path' or 'frames'
        return_video_sample_fps: If True, return tuple of (frames, fps)
    
    Returns:
        torch.Tensor or list[Image.Image]: Video frames
        If return_video_sample_fps is True, returns tuple of (frames, fps)
    """
    import cv2
    import numpy as np
    from PIL import Image
    
    video_path = ele.get('video_path') or ele.get('path')
    
    if not video_path:
        raise ValueError("No video path provided in element")
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(Image.fromarray(frame_rgb))
    
    cap.release()
    
    if not frames:
        raise ValueError(f"No frames extracted from video: {video_path}")
    
    if return_video_sample_fps:
        return frames, fps
    
    return frames