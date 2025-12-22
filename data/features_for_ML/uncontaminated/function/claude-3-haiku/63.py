import os
import numpy as np
from PIL import Image

def save_tensor_to_img(tensor, save_dir):
    """
    Saves a PyTorch tensor as an image file.

    Args:
        tensor (torch.Tensor): The input tensor to be saved as an image.
        save_dir (str): The directory where the image file will be saved.
    """
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Normalize the tensor values to the range [0, 255]
    tensor = (tensor - tensor.min()) / (tensor.max() - tensor.min())
    tensor = (tensor * 255).to(torch.uint8)

    # Convert the tensor to a PIL image and save it
    image = Image.fromarray(tensor.permute(1, 2, 0).byte().numpy())
    image.save(os.path.join(save_dir, "output.png"))