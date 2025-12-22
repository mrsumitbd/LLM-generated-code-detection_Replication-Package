from skimage import transform as trans
import torch
from torchvision.transforms import v2

def warp_affine_torchvision(img, matrix, image_size, rotation_ratio=0.0, border_value=0.0, border_mode='replicate', interpolation_value=v2.functional.InterpolationMode.NEAREST, device='cpu'):
    # Ensure image_size is a tuple (width, height)
    if isinstance(image_size, int):
        image_size = (image_size, image_size)

    # Ensure the image tensor is on the correct device and of type float
    if isinstance(img, torch.Tensor):
        img_tensor = img.to(device).float()
        if img_tensor.dim() == 3:  # If no batch dimension, add one
            img_tensor = img_tensor.unsqueeze(0)
    else:
        img_tensor = torch.from_numpy(img).unsqueeze(0).permute(0, 3, 1, 2).float().to(device)

    # Extract the translation parameters from the affine matrix
    t = trans.SimilarityTransform()
    t.params[0:2] = matrix

    # Define default rotation
    rotation = t.rotation

    if rotation_ratio != 0:
        rotation *=rotation_ratio  # Rotation in degrees

    # Convert border mode
    if border_mode == 'replicate':
        fill = [border_value] * img_tensor.shape[1]  # Same value for all channels
    elif border_mode == 'constant':
        fill = [border_value] * img_tensor.shape[1]  # Same value for all channels
    else:
        raise ValueError("Unsupported border_mode. Use 'replicate' or 'constant'.")

    # Apply the affine transformation
    warped_img_tensor = v2.functional.affine(img_tensor, angle=rotation, translate=(t.translation[0], t.translation[1]), scale=t.scale, shear=(0.0, 0.0), interpolation=interpolation_value, center=(0, 0), fill=fill)

    # Crop the image to the desired size
    warped_img_tensor = v2.functional.crop(warped_img_tensor, 0,0, image_size[1], image_size[0])

    return warped_img_tensor.squeeze(0)