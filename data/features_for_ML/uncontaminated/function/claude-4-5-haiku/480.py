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
    
    processed_windows = []
    
    for window in windows:
        # window shape is (n_samples, channels) or (channels, n_samples)
        # Assume shape is (n_samples, channels)
        if window.ndim == 2:
            if window.shape[1] < window.shape[0]:
                # Likely (channels, n_samples), transpose to (n_samples, channels)
                window = window.T
        
        # Now window should be (n_samples, channels)
        current_channels = window.shape[1] if window.ndim == 2 else 1
        
        if current_channels < n_channels:
            # Pad channels
            pad_width = ((0, 0), (0, n_channels - current_channels))
            window = np.pad(window, pad_width, mode='constant', constant_values=0)
        elif current_channels > n_channels:
            # Trim channels
            window = window[:, :n_channels]
        
        # Transpose to (channels, n_samples)
        if window.ndim == 2:
            window = window.T
        
        processed_windows.append(window)
    
    # Stack into batch and convert to tensor
    batch = np.stack(processed_windows, axis=0)
    tensor = torch.from_numpy(batch).float().to(device)
    
    return tensor