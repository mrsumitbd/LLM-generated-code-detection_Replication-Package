import torch
from PIL import Image
import cv2

def fetch_video(
    ele: dict, return_video_sample_fps: bool = False
) -> torch.Tensor | list[Image.Image]:
    video_path = ele['video_path']
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frames.append(frame)
    cap.release()
    video_tensor = torch.stack([torch.from_numpy(np.array(frame)) for frame in frames])
    if return_video_sample_fps:
        fps = cap.get(cv2.CAP_PROP_FPS)
        return video_tensor, fps
    else:
        return video_tensor