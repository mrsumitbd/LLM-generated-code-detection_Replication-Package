def warp_affine_torchvision(img, matrix, image_size, rotation_ratio=0.0, border_value=0.0, border_mode='replicate', interpolation_value=v2.functional.InterpolationMode.NEAREST, device='cpu'):
    # Ensure image_size is a tuple (width, height)
    if isinstance(image_size, int):
        image_size = (image_size, image_size)
    
    # Convert image to tensor if it's a PIL Image
    if isinstance(img, Image.Image):
        img_tensor = v2.functional.to_image(img)
    elif isinstance(img, np.ndarray):
        img_tensor = torch.from_numpy(img).permute(2, 0, 1) if img.ndim == 3 else torch.from_numpy(img).unsqueeze(0)
    else:
        img_tensor = img
    
    # Ensure tensor is on the correct device
    if isinstance(img_tensor, torch.Tensor):
        img_tensor = img_tensor.to(device)
    
    # Convert matrix to tensor if needed
    if isinstance(matrix, np.ndarray):
        matrix_tensor = torch.from_numpy(matrix).float().to(device)
    else:
        matrix_tensor = matrix.float().to(device)
    
    # Ensure matrix is 2x3
    if matrix_tensor.shape == (3, 3):
        matrix_tensor = matrix_tensor[:2, :]
    
    # Add batch dimension if needed
    if img_tensor.ndim == 3:
        img_tensor = img_tensor.unsqueeze(0)
    
    # Apply affine transformation using torchvision
    output = v2.functional.affine(
        img_tensor,
        angle=0,
        translate=(0, 0),
        scale=1.0,
        shear=0,
        interpolation=interpolation_value,
        fill=border_value
    )
    
    # Use warp_affine directly with the transformation matrix
    # Reshape matrix for warp_affine (needs to be Nx2x3)
    if matrix_tensor.ndim == 2:
        matrix_tensor = matrix_tensor.unsqueeze(0)
    
    # Apply warp_affine
    output = v2.functional.warp_affine(
        img_tensor,
        matrix_tensor,
        image_size,
        interpolation=interpolation_value,
        fill=border_value,
        padding_mode=border_mode
    )
    
    # Remove batch dimension if input didn't have it
    if output.shape[0] == 1:
        output = output.squeeze(0)
    
    return output