import random
from typing import Tuple, Optional

import numpy as np
from PIL import Image
import torchvision.transforms as T

# If TARGET_IMAGE_SIZE is defined elsewhere, use it; otherwise default to 224
try:
    from config import TARGET_IMAGE_SIZE  # type: ignore
except Exception:
    TARGET_IMAGE_SIZE = 224


def _mask_at_point(img: Image.Image, point: Tuple[int, int], size: int = 10) -> Image.Image:
    """Mask a square region around `point` in the image."""
    arr = np.array(img)
    h, w = arr.shape[:2]
    x, y = point
    half = size // 2
    x0 = max(0, x - half)
    y0 = max(0, y - half)
    x1 = min(w, x + half)
    y1 = min(h, y + half)
    arr[y0:y1, x0:x1] = 0
    return Image.fromarray(arr)


def get_random_augmentations(
    target_image_size: int = TARGET_IMAGE_SIZE,
    mask_point: Optional[Tuple[int, int]] = None,
):
    """
    Return a torchvision.transforms.Compose object that applies a random set of
    augmentations to an image.

    Parameters
    ----------
    target_image_size : int, optional
        The size to which the image will be resized (default: TARGET_IMAGE_SIZE).
    mask_point : tuple[int, int] or None, optional
        If provided, a square mask of size 10x10 will be applied around this
        point in the image.

    Returns
    -------
    torchvision.transforms.Compose
        A composed transform that can be applied to a PIL.Image.
    """
    transforms = []

    # Resize and random crop
    transforms.append(T.RandomResizedCrop(target_image_size, scale=(0.8, 1.0), ratio=(0.75, 1.33)))

    # Random flips
    transforms.append(T.RandomHorizontalFlip(p=0.5))
    transforms.append(T.RandomVerticalFlip(p=0.5))

    # Random rotation
    transforms.append(T.RandomRotation(degrees=15))

    # Color jitter
    transforms.append(
        T.ColorJitter(
            brightness=0.2,
            contrast=0.2,
            saturation=0.2,
            hue=0.1,
        )
    )

    # Optional mask
    if mask_point is not None:
        transforms.append(
            T.Lambda(lambda img: _mask_at_point(img, mask_point, size=10))
        )

    # Convert to tensor and normalize
    transforms.append(T.ToTensor())
    transforms.append(
        T.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        )
    )

    return T.Compose(transforms)