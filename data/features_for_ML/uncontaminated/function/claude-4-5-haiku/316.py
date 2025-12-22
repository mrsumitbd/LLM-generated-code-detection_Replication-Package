import torch
from ultralytics import YOLO
from PIL import Image
import numpy as np

def load_detector_by_name(detector_name, *, resize=1024, weights_path=None):
    """
    Load a detector model by name.
    
    Args:
        detector_name: Name of the detector model (e.g., 'yolov8n', 'yolov8s', etc.)
        resize: Image resize dimension (default: 1024)
        weights_path: Path to custom weights file (optional)
    
    Returns:
        A detector object with predict method
    """
    
    class YOLODetector:
        def __init__(self, model_name, resize_dim, weights):
            self.resize = resize_dim
            if weights:
                self.model = YOLO(weights)
            else:
                self.model = YOLO(f'{model_name}.pt')
        
        def predict(self, image_input):
            """
            Run detection on an image.
            
            Args:
                image_input: PIL Image, numpy array, or file path
            
            Returns:
                Detection results
            """
            if isinstance(image_input, str):
                image = Image.open(image_input)
            elif isinstance(image_input, Image.Image):
                image = image_input
            elif isinstance(image_input, np.ndarray):
                image = Image.fromarray(image_input)
            else:
                image = image_input
            
            results = self.model.predict(image, imgsz=self.resize, verbose=False)
            return results
    
    return YOLODetector(detector_name, resize, weights_path)