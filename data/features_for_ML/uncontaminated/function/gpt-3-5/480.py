import numpy as np
import torch

def prepare_batch_for_eegpt(windows, n_channels=20, device="cpu"):
    max_samples = max(window.shape[1] for window in windows)
    padded_windows = [np.pad(window, ((0, 0), (0, max_samples - window.shape[1])), mode='constant') for window in windows]
    batch_tensor = torch.tensor(padded_windows, dtype=torch.float64, device=device)
    return batch_tensor.permute(0, 2, 1)

# Test the function with an example
windows = [np.random.rand(20, 100) for _ in range(5)]
batch_tensor = prepare_batch_for_eegpt(windows, n_channels=20, device="cpu")
print(batch_tensor.shape)