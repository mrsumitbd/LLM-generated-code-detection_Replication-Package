import torch
import torchvision
from torchvision import transforms
from PIL import Image
import os

class DetectorWrapper:
    """Simple wrapper around a torchvision detection model."""
    def __init__(self, model, resize=1024):
        self.model = model
        self.resize = resize
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((resize, resize)),
            transforms.ToTensor(),
        ])

    def __call__(self, image):
        """
        Run detection on a PIL.Image or numpy array.
        Returns the raw model output.
        """
        if isinstance(image, Image.Image):
            img = image
        else:
            # Assume numpy array
            img = Image.fromarray(image)
        img_t = self.transform(img).unsqueeze(0)
        with torch.no_grad():
            return self.model(img_t)[0]

def _load_torchvision_detector(name, weights_path=None):
    if name == "fasterrcnn":
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)
        if weights_path:
            state = torch.load(weights_path, map_location="cpu")
            model.load_state_dict(state)
        else:
            # Load default pretrained weights
            model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        return model
    if name == "ssd":
        model = torchvision.models.detection.ssd300_vgg16(pretrained=False)
        if weights_path:
            state = torch.load(weights_path, map_location="cpu")
            model.load_state_dict(state)
        else:
            model = torchvision.models.detection.ssd300_vgg16(pretrained=True)
        return model
    if name == "retinanet":
        model = torchvision.models.detection.retinanet_resnet50_fpn(pretrained=False)
        if weights_path:
            state = torch.load(weights_path, map_location="cpu")
            model.load_state_dict(state)
        else:
            model = torchvision.models.detection.retinanet_resnet50_fpn(pretrained=True)
        return model
    raise ValueError(f"Unsupported torchvision detector name: {name}")

def _load_ultralytics_detector(name, weights_path=None):
    try:
        from ultralytics import YOLO
    except Exception as e:
        raise ImportError("ultralytics package is required for YOLO detectors") from e
    if name == "yolo":
        if weights_path:
            if not os.path.exists(weights_path):
                raise FileNotFoundError(f"YOLO weights not found: {weights_path}")
            model = YOLO(weights_path)
        else:
            # Default YOLOv8n
            model = YOLO("yolov8n.pt")
        return model
    raise ValueError(f"Unsupported ultralytics detector name: {name}")

def load_detector_by_name(detector_name, *, resize=1024, weights_path=None):
    """
    Load a detector by name.

    Parameters
    ----------
    detector_name : str
        Name of the detector. Supported names:
        - "fasterrcnn"
        - "ssd"
        - "retinanet"
        - "yolo"

    resize : int, optional
        Resize dimension for input images. Default is 1024.

    weights_path : str or None, optional
        Path to a custom weights file. If None, default pretrained weights are used.

    Returns
    -------
    detector : object
        A detector object that can be called with a PIL.Image or numpy array.
    """
    name = detector_name.lower()
    if name in {"fasterrcnn", "ssd", "retinanet"}:
        model = _load_torchvision_detector(name, weights_path)
        return DetectorWrapper(model, resize=resize)
    if name == "yolo":
        model = _load_ultralytics_detector(name, weights_path)
        # Ultralytics YOLO models already handle resizing internally.
        # Wrap to keep API consistent.
        class YOLOWrapper:
            def __init__(self, model):
                self.model = model
            def __call__(self, image):
                # Ultralytics expects numpy array or PIL.Image
                return self.model(image)[0]
        return YOLOWrapper(model)
    raise ValueError(f"Unsupported detector name: {detector_name}")