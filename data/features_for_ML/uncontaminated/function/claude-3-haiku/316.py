import os
from pathlib import Path
from typing import Optional

from .detector import Detector
from .yolo_detector import YOLODetector
from .ssd_detector import SSDDetector

def load_detector_by_name(detector_name: str, *, resize: int = 1024, weights_path: Optional[str] = None) -> Detector:
    """
    Load a detector object based on the provided detector name.

    Args:
        detector_name (str): The name of the detector to load.
        resize (int, optional): The size to resize the input images to. Defaults to 1024.
        weights_path (str, optional): The path to the pre-trained weights file. If not provided, the default weights will be used.

    Returns:
        Detector: The loaded detector object.
    """
    if detector_name.lower() == "yolo":
        return YOLODetector(resize=resize, weights_path=weights_path)
    elif detector_name.lower() == "ssd":
        return SSDDetector(resize=resize, weights_path=weights_path)
    else:
        raise ValueError(f"Unsupported detector name: {detector_name}")