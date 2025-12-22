import numpy as np
import numpy.typing as npt
import torch
import torch

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
    import torch

    batch_list = []
    for window in windows:
        current_channels = window.shape[0]

        # Pad or trim channels
        if current_channels < n_channels:
            # Pad with zeros
            padding = np.zeros((n_channels - current_channels, window.shape[1]))
            window = np.vstack([window, padding])
        elif current_channels > n_channels:
            # Trim to first n_channels
            window = window[:n_channels]

        batch_list.append(window)

    # Stack into batch
    batch = np.stack(batch_list, axis=0)

    # Convert to tensor
    batch_tensor = torch.from_numpy(batch).float()

    if device != "cpu":
        batch_tensor = batch_tensor.to(device)

    return batch_tensor