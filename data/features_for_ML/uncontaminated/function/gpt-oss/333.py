import torch

def add_fourier_features(inputs: torch.Tensor, start=6, stop=8, step=1):
    """
    Append sine and cosine Fourier features to the input tensor.

    Parameters
    ----------
    inputs : torch.Tensor
        Tensor of shape (..., D) where D is the number of input features.
    start : int, optional
        Starting frequency multiplier (inclusive). Default is 6.
    stop : int, optional
        Stopping frequency multiplier (exclusive). Default is 8.
    step : int, optional
        Step size between frequency multipliers. Default is 1.

    Returns
    -------
    torch.Tensor
        Tensor of shape (..., D + 2 * D * num_frequencies) containing the original
        features followed by sine and cosine features for each frequency.
    """
    # Ensure inputs are float for trig functions
    inputs = inputs.to(torch.float32)

    # Create frequency multipliers
    freqs = torch.arange(start, stop, step, dtype=inputs.dtype, device=inputs.device)

    # If no frequencies are provided, just return the original inputs
    if freqs.numel() == 0:
        return inputs

    # Expand dimensions for broadcasting: (..., D, 1) * (1, 1, F) -> (..., D, F)
    expanded_inputs = inputs.unsqueeze(-1)  # (..., D, 1)
    scaled = expanded_inputs * freqs  # (..., D, F)

    # Compute sine and cosine features
    sin_features = torch.sin(scaled)   # (..., D, F)
    cos_features = torch.cos(scaled)   # (..., D, F)

    # Reshape to (..., D * F) for each of sin and cos
    sin_flat = sin_features.reshape(*inputs.shape[:-1], -1)
    cos_flat = cos_features.reshape(*inputs.shape[:-1], -1)

    # Concatenate original inputs with sin and cos features
    return torch.cat([inputs, sin_flat, cos_flat], dim=-1)