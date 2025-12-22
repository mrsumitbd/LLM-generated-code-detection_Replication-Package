def warp_affine_torchvision(img, matrix, image_size, rotation_ratio=0.0, border_value=0.0, border_mode='replicate', interpolation_value=v2.functional.InterpolationMode.NEAREST, device='cpu'):
    import torch
    import torchvision.transforms.functional as v2
    
    if not isinstance(image_size, tuple):
        image_size = (image_size, image_size)
    
    img = v2.to_pil_image(img)
    img = v2.affine(img, matrix, image_size, interpolation=interpolation_value, fill=border_value, resample=0, fillcolor=None)
    
    return v2.to_tensor(img).to(device)