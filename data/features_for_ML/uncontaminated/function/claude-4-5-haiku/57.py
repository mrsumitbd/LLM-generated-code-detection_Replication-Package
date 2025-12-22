def pil_to_tensor(image):
    # Takes a PIL image and returns a tensor of shape [1, height, width, channels]
    import torch
    import numpy as np
    
    # Convert PIL image to numpy array
    image_array = np.array(image)
    
    # Add batch dimension at the beginning
    tensor = torch.from_numpy(image_array).unsqueeze(0)
    
    # Convert to float and normalize to [0, 1] if needed
    if tensor.dtype == torch.uint8:
        tensor = tensor.float() / 255.0
    
    return tensor