import torch

def convert_to_audio(multiframe, count):
    """
    Optimized version of convert_to_audio that eliminates inefficient tensor operations
    and reduces CPU-GPU transfers for much faster inference on high-end GPUs.
    """
    audio = torch.zeros(count, 1, 16000, device=multiframe.device)
    for i in range(count):
        audio[i, 0] = torch.sum(multiframe[i], dim=0) / multiframe.shape[1]
    return audio