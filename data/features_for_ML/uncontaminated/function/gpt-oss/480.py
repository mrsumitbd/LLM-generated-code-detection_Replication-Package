import numpy as np
import numpy.typing as npt
import torch

def prepare_batch_for_eegpt(
    windows: list[npt.NDArray[np.float64]],
    n_channels: int = 20,
    device: str = "cpu",
) -> "torch.Tensor":
    """
    Prepare a batch of windows for EEGPT input.

    Args:
        windows: List of EEG windows (each a 2‑D numpy array of shape (channels, samples)).
        n_channels: Target number of channels (pad/trim as needed).
        device: Device to place tensor on.

    Returns:
        Batch tensor of shape (batch_size, n_channels, n_samples).
    """
    if not windows:
        raise ValueError("windows list is empty")

    # Determine maximum number of samples across all windows
    max_samples = max(w.shape[1] for w in windows)

    processed = []
    for w in windows:
        # Ensure 2‑D array
        if w.ndim != 2:
            raise ValueError(f"Each window must be 2‑D, got shape {w.shape}")

        ch, samp = w.shape

        # Pad or trim channels
        if ch < n_channels:
            pad_ch = n_channels - ch
            w_ch = np.pad(w, ((0, pad_ch), (0, 0)), mode="constant", constant_values=0)
        else:
            w_ch = w[:n_channels, :]

        # Pad samples to max_samples
        if samp < max_samples:
            pad_samp = max_samples - samp
            w_ch = np.pad(w_ch, ((0, 0), (0, pad_samp)), mode="constant", constant_values=0)
        else:
            w_ch = w_ch[:, :max_samples]

        processed.append(w_ch.astype(np.float32))

    # Stack into tensor
    batch_np = np.stack(processed, axis=0)  # shape (batch, n_channels, n_samples)
    batch_torch = torch.from_numpy(batch_np).to(device=device, dtype=torch.float32)

    return batch_torch