import os
import torch
import torchvision.transforms as transforms
from PIL import Image


def save_tensor_to_img(tensor, save_dir):
    """
    Save a tensor as an image file.
    
    Args:
        tensor: A torch tensor representing an image
        save_dir: Directory path where the image will be saved
    """
    os.makedirs(save_dir, exist_ok=True)
    
    if isinstance(tensor, torch.Tensor):
        tensor = tensor.cpu().detach()
        
        if tensor.dim() == 4:
            tensor = tensor.squeeze(0)
        
        if tensor.shape[0] in [1, 3, 4]:
            if tensor.shape[0] == 1:
                tensor = tensor.squeeze(0)
            else:
                tensor = tensor.permute(1, 2, 0)
        
        if tensor.dtype == torch.float32 or tensor.dtype == torch.float64:
            tensor = torch.clamp(tensor, 0, 1)
            tensor = (tensor * 255).to(torch.uint8)
        
        img_array = tensor.numpy()
    else:
        img_array = tensor
    
    img = Image.fromarray(img_array)
    
    img_path = os.path.join(save_dir, "output.png")
    img.save(img_path)
    
    return img_path