def get_random_augmentations(target_image_size=TARGET_IMAGE_SIZE, mask_point=None):
    import random
    
    if mask_point is None:
        mask_point = (random.randint(0, target_image_size[0]), random.randint(0, target_image_size[1]))
    
    return target_image_size, mask_point