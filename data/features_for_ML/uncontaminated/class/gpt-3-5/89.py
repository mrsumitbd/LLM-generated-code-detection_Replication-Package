from typing import Union
import numpy as np
import base64
import cv2

class ImageUtils:

    @staticmethod
    def format_image(image: Union[str, np.ndarray]):
        if isinstance(image, str):
            return cv2.imread(image)
        elif isinstance(image, np.ndarray):
            return image
        else:
            raise ValueError("Invalid image format. Please provide a valid image path or numpy array.")

    @staticmethod
    def numpy2base64(video_frame, format="JPEG"):
        _, buffer = cv2.imencode(".jpg", video_frame)
        return base64.b64encode(buffer).decode()

    @staticmethod
    def save_base64_image(base64_data, output_path):
        with open(output_path, "wb") as file:
            file.write(base64.b64decode(base64_data))