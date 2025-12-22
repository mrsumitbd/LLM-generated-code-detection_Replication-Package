import torch
import numpy as np
import numpy.typing as npt

def prepare_batch_for_eegpt(
    windows: list[npt.NDArray[np.float64]], n_channels: int = 20, device: str = "cpu"
) -> "torch.Tensor":
    """Prepare a batch of windows for EEGPT input.

    Args:
        windows: List of EEG windows
        n_channels: Target number of channels (pad/trim as needed)
        device: Device to place tensor on

    Returns:
        Batch tensor of shape (batch_size, n_channels, n_samples)
    """
    batch_size = len(windows)
    n_samples = max(window.shape[1] for window in windows)

    batch = torch.zeros(batch_size, n_channels, n_samples, device=device)

    for i, window in enumerate(windows):
        n_window_channels = window.shape[0]
        if n_window_channels > n_channels:
            batch[i, :, :] = torch.from_numpy(window[:n_channels, :]).to(device)
        else:
            batch[i, :n_window_channels, :] = torch.from_numpy(window).to(device)
            batch[i, n_window_channels:, :] = 0

    return batch