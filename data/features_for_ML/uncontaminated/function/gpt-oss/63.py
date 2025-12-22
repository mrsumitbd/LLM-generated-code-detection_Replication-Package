import os
import time
import uuid
import numpy as np
from PIL import Image

try:
    import torch
except ImportError:
    torch = None

def save_tensor_to_img(tensor, save_dir):
    """
    Save a tensor (PyTorch or NumPy) as an image file in the specified directory.

    Parameters
    ----------
    tensor : torch.Tensor or np.ndarray
        The image tensor. Expected shapes:
            - (C, H, W) or (H, W) for a single image
            - (N, C, H, W) for a batch (only the first image is saved)
    save_dir : str
        Directory where the image will be saved. It will be created if it does not exist.

    Returns
    -------
    str
        Full path to the saved image file.
    """
    # Ensure the directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Convert torch tensor to numpy if necessary
    if torch is not None and isinstance(tensor, torch.Tensor):
        tensor = tensor.detach().cpu()
        if tensor.ndim == 4:  # batch
            tensor = tensor[0]
        if tensor.ndim == 3 and tensor.shape[0] in {1, 3, 4}:
            # (C, H, W) -> (H, W, C)
            tensor = tensor.permute(1, 2, 0)
        elif tensor.ndim == 2:
            # (H, W) stays the same
            pass
        else:
            raise ValueError(f"Unsupported tensor shape: {tensor.shape}")
        tensor = tensor.numpy()
    elif isinstance(tensor, np.ndarray):
        if tensor.ndim == 4:  # batch
            tensor = tensor[0]
        if tensor.ndim == 3 and tensor.shape[0] in {1, 3, 4}:
            tensor = np.transpose(tensor, (1, 2, 0))
        elif tensor.ndim == 2:
            pass
        else:
            raise ValueError(f"Unsupported array shape: {tensor.shape}")
    else:
        raise TypeError("tensor must be a torch.Tensor or np.ndarray")

    # Handle data type and scaling
    if np.issubdtype(tensor.dtype, np.floating):
        # Assume values are in [0, 1]
        tensor = np.clip(tensor, 0, 1)
        tensor = (tensor * 255).astype(np.uint8)
    elif np.issubdtype(tensor.dtype, np.integer):
        # Assume values are already in [0, 255]
        tensor = np.clip(tensor, 0, 255).astype(np.uint8)
    else:
        raise TypeError(f"Unsupported tensor dtype: {tensor.dtype}")

    # Create PIL image
    if tensor.ndim == 2:
        mode = "L"
    elif tensor.shape[2] == 3:
        mode = "RGB"
    elif tensor.shape[2] == 4:
        mode = "RGBA"
    else:
        raise ValueError(f"Unsupported channel dimension: {tensor.shape[2]}")

    img = Image.fromarray(tensor, mode=mode)

    # Generate unique filename
    filename = f"image_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}.png"
    filepath = os.path.join(save_dir, filename)

    # Save image
    img.save(filepath)

    return filepath