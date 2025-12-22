import torch
import torchvision.transforms.v2.functional as v2f
from torchvision.transforms.v2 import InterpolationMode

def warp_affine_torchvision(
    img,
    matrix,
    image_size,
    rotation_ratio=0.0,
    border_value=0.0,
    border_mode='replicate',
    interpolation_value=InterpolationMode.NEAREST,
    device='cpu'
):
    """
    Apply an affine warp to an image using torchvision's grid_sample.

    Parameters
    ----------
    img : torch.Tensor
        Image tensor of shape (C, H, W) or (B, C, H, W).
    matrix : torch.Tensor
        Affine transformation matrix of shape (2, 3).
    image_size : tuple[int, int]
        Desired output size as (width, height).
    rotation_ratio : float, optional
        Not used in this implementation (kept for API compatibility).
    border_value : float, optional
        Value to use for padding when border_mode is 'zeros'.
    border_mode : str, optional
        One of 'replicate', 'zeros', 'reflection'.
    interpolation_value : InterpolationMode, optional
        Interpolation mode for grid_sample.
    device : str or torch.device, optional
        Device on which to perform the operation.

    Returns
    -------
    torch.Tensor
        Warped image tensor of shape (C, H_out, W_out) or (B, C, H_out, W_out).
    """
    # Ensure image_size is a tuple (width, height)
    if not (isinstance(image_size, tuple) and len(image_size) == 2):
        raise ValueError("image_size must be a tuple of (width, height)")

    # Move to device
    device = torch.device(device)
    img = img.to(device)

    # Ensure matrix is on device
    matrix = matrix.to(device)

    # Handle batch dimension
    if img.dim() == 3:
        img = img.unsqueeze(0)  # (1, C, H, W)
    elif img.dim() != 4:
        raise ValueError("img must be a 3D or 4D tensor")

    B, C, H_in, W_in = img.shape

    # Prepare affine matrix for grid_sample
    # matrix shape should be (B, 2, 3)
    affine_mat = matrix.unsqueeze(0).expand(B, -1, -1)  # (B, 2, 3)

    # Desired output size
    out_w, out_h = image_size
    out_size = (B, C, out_h, out_w)

    # Create grid
    grid = torch.nn.functional.affine_grid(
        affine_mat,
        size=out_size,
        align_corners=False
    )

    # Map interpolation mode
    interp_map = {
        InterpolationMode.NEAREST: 'nearest',
        InterpolationMode.BILINEAR: 'bilinear',
        InterpolationMode.BICUBIC: 'bicubic',
    }
    interp_mode = interp_map.get(interpolation_value, 'nearest')

    # Map border mode
    border_map = {
        'replicate': 'border',
        'border': 'border',
        'zeros': 'zeros',
        'zero': 'zeros',
        'reflection': 'reflection',
        'reflect': 'reflection',
    }
    padding_mode = border_map.get(border_mode.lower(), 'border')

    # If border_value is non-zero and padding_mode is zeros, we need to pad manually
    if border_value != 0.0 and padding_mode == 'zeros':
        # Pad image with constant border_value
        pad = (0, 0, 0, 0)  # no padding needed for grid_sample
        img = torch.nn.functional.pad(img, pad, mode='constant', value=border_value)

    # Perform sampling
    warped = torch.nn.functional.grid_sample(
        img,
        grid,
        mode=interp_mode,
        padding_mode=padding_mode,
        align_corners=False
    )

    # Remove batch dimension if original image was 3D
    if warped.shape[0] == 1 and img.shape[0] == 1:
        warped = warped.squeeze(0)

    return warped