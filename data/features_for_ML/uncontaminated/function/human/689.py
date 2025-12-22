import torchvision.transforms as transforms
from natix.validator.config import TARGET_IMAGE_SIZE

def get_random_augmentations(target_image_size=TARGET_IMAGE_SIZE, mask_point=None):
    return ComposeWithParams(
        [
            ConvertToRGB(),
            transforms.ToTensor(),
            RandomRotationWithParams(20, interpolation=transforms.InterpolationMode.BILINEAR),
            RandomResizedCropWithParams(TARGET_IMAGE_SIZE, scale=(0.2, 1.0), ratio=(1.0, 1.0), include_point=mask_point),
            RandomHorizontalFlipWithParams(),
            RandomVerticalFlipWithParams(),
        ]
    )