import base64
import cv2
import numpy as np
from typing import Union
from pathlib import Path


class ImageUtils:

    @staticmethod
    def format_image(image: Union[str, np.ndarray]):
        if isinstance(image, str):
            image = cv2.imread(image)
            if image is None:
                raise ValueError(f"Failed to read image from path: {image}")
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif isinstance(image, np.ndarray):
            if len(image.shape) == 3 and image.shape[2] == 3:
                if image.dtype == np.uint8:
                    pass
                else:
                    image = (image * 255).astype(np.uint8)
            elif len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            raise TypeError(f"Unsupported image type: {type(image)}")
        
        return image

    @staticmethod
    def numpy2base64(video_frame, format="JPEG"):
        if isinstance(video_frame, np.ndarray):
            if len(video_frame.shape) == 3 and video_frame.shape[2] == 3:
                video_frame = cv2.cvtColor(video_frame, cv2.COLOR_RGB2BGR)
            
            success, buffer = cv2.imencode(f".{format.lower()}", video_frame)
            if not success:
                raise ValueError(f"Failed to encode image to {format}")
            
            base64_data = base64.b64encode(buffer).decode('utf-8')
            return base64_data
        else:
            raise TypeError(f"Expected numpy array, got {type(video_frame)}")

    @staticmethod
    def save_base64_image(base64_data, output_path):
        try:
            image_data = base64.b64decode(base64_data)
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            return True
        except Exception as e:
            raise ValueError(f"Failed to save base64 image: {str(e)}")