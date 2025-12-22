import random
import numpy as np
from albumentations import (
    Compose,
    RandomBrightnessContrast,
    RandomRotate90,
    Flip,
    Transpose,
    Normalize,
    Resize,
)

def get_random_augmentations(target_image_size=TARGET_IMAGE_SIZE, mask_point=None):
    augmentations = Compose([
        Resize(target_image_size[0], target_image_size[1]),
        RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
        RandomRotate90(p=0.5),
        Flip(p=0.5),
        Transpose(p=0.5),
        Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225], p=1.0),
    ])

    if mask_point is not None:
        mask_size = (int(target_image_size[0] * 0.2), int(target_image_size[1] * 0.2))
        mask_x = random.randint(0, target_image_size[0] - mask_size[0])
        mask_y = random.randint(0, target_image_size[1] - mask_size[1])
        mask = np.zeros((target_image_size[0], target_image_size[1], 1), dtype=np.uint8)
        mask[mask_y:mask_y + mask_size[1], mask_x:mask_x + mask_size[0]] = 255
        augmentations.add_targets({"mask": mask_point})

    return augmentations