import os
import base64
from typing import Union

import numpy as np
import cv2


class ImageUtils:
    @staticmethod
    def format_image(image: Union[str, np.ndarray]) -> np.ndarray:
        """
        Convert an image input to a NumPy array.

        Parameters
        ----------
        image : Union[str, np.ndarray]
            Either a file path to an image or a NumPy array.

        Returns
        -------
        np.ndarray
            The image as a NumPy array in BGR format.
        """
        if isinstance(image, str):
            img = cv2.imread(image, cv2.IMREAD_COLOR)
            if img is None:
                raise FileNotFoundError(f"Unable to read image from path: {image}")
            return img
        elif isinstance(image, np.ndarray):
            if image.dtype != np.uint8:
                img = image.astype(np.uint8)
            else:
                img = image
            return img
        else:
            raise TypeError("image must be a file path string or a NumPy array")

    @staticmethod
    def numpy2base64(video_frame: np.ndarray, format: str = "JPEG") -> str:
        """
        Encode a NumPy image array to a base64 string.

        Parameters
        ----------
        video_frame : np.ndarray
            The image array to encode.
        format : str, optional
            The image format to use for encoding (default: "JPEG").

        Returns
        -------
        str
            Base64 encoded string of the image.
        """
        if not isinstance(video_frame, np.ndarray):
            raise TypeError("video_frame must be a NumPy array")

        ext = f".{format.lower()}"
        success, buffer = cv2.imencode(ext, video_frame)
        if not success:
            raise ValueError(f"Could not encode image to format {format}")

        b64_bytes = base64.b64encode(buffer.tobytes())
        return b64_bytes.decode("utf-8")

    @staticmethod
    def save_base64_image(base64_data: str, output_path: str) -> None:
        """
        Decode a base64 image string and save it to disk.

        Parameters
        ----------
        base64_data : str
            Base64 encoded image data.
        output_path : str
            Path where the image will be saved.
        """
        if not isinstance(base64_data, str):
            raise TypeError("base64_data must be a string")

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        image_bytes = base64.b64decode(base64_data)
        # Convert bytes to a NumPy array and decode to image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Decoded image is invalid")

        # Write the image to the specified path
        success = cv2.imwrite(output_path, img)
        if not success:
            raise IOError(f"Failed to write image to {output_path}")