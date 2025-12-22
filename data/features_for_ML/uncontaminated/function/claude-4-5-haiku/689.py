def get_random_augmentations(target_image_size=TARGET_IMAGE_SIZE, mask_point=None):
    """
    Returns a composition of random augmentations for image data.
    
    Args:
        target_image_size: Target size for resizing images
        mask_point: Optional mask point for augmentation
    
    Returns:
        A composition of augmentation transforms
    """
    import albumentations as A
    from albumentations.pytorch import ToTensorV2
    
    augmentations = [
        A.RandomResizedCrop(
            height=target_image_size,
            width=target_image_size,
            scale=(0.8, 1.0),
            p=0.5
        ),
        A.Resize(height=target_image_size, width=target_image_size),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        A.Rotate(limit=30, p=0.5),
        A.GaussNoise(p=0.2),
        A.GaussianBlur(blur_limit=3, p=0.2),
        A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1, p=0.5),
        A.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        ),
        ToTensorV2()
    ]
    
    return A.Compose(augmentations)