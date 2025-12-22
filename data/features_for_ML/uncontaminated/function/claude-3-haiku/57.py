import torch

def pil_to_tensor(image):
    # Takes a PIL image and returns a tensor of shape [1, height, width, channels]
    tensor = torch.from_numpy(image.convert('RGB')).permute(2, 0, 1).unsqueeze(0)
    return tensor