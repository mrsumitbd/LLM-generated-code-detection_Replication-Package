import torch

def log_norm(x, mean=-4, std=4, dim=2):
    """
    Convert a normalized log‑mel spectrogram back to the log‑mel domain after
    normalising the linear‑mel spectrogram.

    Parameters
    ----------
    x : torch.Tensor
        Normalised log‑mel spectrogram (log domain).
    mean : float, optional
        Mean used for normalising the linear‑mel spectrogram. Default is -4.
    std : float, optional
        Standard deviation used for normalising the linear‑mel spectrogram.
        Default is 4.
    dim : int, optional
        Dimension along which to compute the mean and std if `mean` and `std`
        are tensors. (Not used when `mean` and `std` are scalars.)

    Returns
    -------
    torch.Tensor
        The log of the normalised linear‑mel spectrogram.
    """
    # Convert from log‑mel to linear‑mel
    mel = torch.exp(x)

    # Normalise the linear‑mel spectrogram
    # If mean/std are scalars, use them directly; otherwise compute along dim
    if isinstance(mean, torch.Tensor) or isinstance(std, torch.Tensor):
        # Compute mean and std along the specified dimension if not provided
        if mean is None:
            mean = mel.mean(dim=dim, keepdim=True)
        if std is None:
            std = mel.std(dim=dim, keepdim=True)
        norm = (mel - mean) / (std + 1e-8)
    else:
        norm = (mel - mean) / (std + 1e-8)

    # Avoid log of non‑positive values
    eps = 1e-8
    norm = torch.clamp(norm, min=eps)

    # Return the log of the normalised spectrogram
    return torch.log(norm)