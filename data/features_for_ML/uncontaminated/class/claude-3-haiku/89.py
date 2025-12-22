import base64
import cv2
import numpy as np
from typing import Union

class ImageUtils:

    @staticmethod
    def format_image(image: Union[str, np.ndarray]):
        if isinstance(image, str):
            image = cv2.imread(image)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    @staticmethod
    def numpy2base64(video_frame, format="JPEG"):
        _, buffer = cv2.imencode(f".{format}", video_frame)
        return base64.b64encode(buffer).decode("utf-8")

    @staticmethod
    def save_base64_image(base64_data, output_path):
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(base64_data))