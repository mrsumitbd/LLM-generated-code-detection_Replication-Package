import torch
import torch.nn.functional as F

def warp_affine_torchvision(img, matrix, image_size, rotation_ratio=0.0, border_value=0.0, border_mode='replicate', interpolation_value=F.InterpolationMode.NEAREST, device='cpu'):
    # Ensure image_size is a tuple (width, height)
    if not isinstance(image_size, tuple):
        image_size = (image_size, image_size)

    # Convert the input image to a PyTorch tensor
    img_tensor = torch.as_tensor(img, device=device)

    # Rotate the transformation matrix if rotation_ratio is provided
    if rotation_ratio != 0.0:
        angle = rotation_ratio * 360
        rotation_matrix = torch.tensor([[torch.cos(torch.radians(angle)), -torch.sin(torch.radians(angle)), 0],
                                       [torch.sin(torch.radians(angle)), torch.cos(torch.radians(angle)), 0]],
                                      device=device)
        matrix = torch.matmul(matrix, rotation_matrix)

    # Perform the affine transformation
    output_size = (image_size[1], image_size[0])
    output_tensor = F.grid_sample(img_tensor.unsqueeze(0), F.affine_grid(matrix.unsqueeze(0), output_size, align_corners=True),
                                  mode=interpolation_value.value, padding_mode=border_mode, value=border_value)

    # Return the transformed image
    return output_tensor.squeeze(0).cpu().numpy()