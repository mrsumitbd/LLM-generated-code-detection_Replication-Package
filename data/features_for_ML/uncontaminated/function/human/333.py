import torch
import torch

def add_fourier_features(inputs: torch.Tensor, start=6, stop=8, step=1):
    num_freqs = (stop - start) // step
    assert inputs.ndim == 5
    C = inputs.size(1)

    # Create Base 2 Fourier features.
    freqs = torch.arange(start, stop, step, dtype=inputs.dtype, device=inputs.device)
    assert num_freqs == len(freqs)
    w = torch.pow(2.0, freqs) * (2 * torch.pi)  # [num_freqs]
    C = inputs.shape[1]
    w = w.repeat(C)[None, :, None, None, None]  # [1, C * num_freqs, 1, 1, 1]

    # Interleaved repeat of input channels to match w.
    h = inputs.repeat_interleave(num_freqs, dim=1)  # [B, C * num_freqs, T, H, W]
    # Scale channels by frequency.
    h = w * h

    return torch.cat(
        [
            inputs,
            torch.sin(h),
            torch.cos(h),
        ],
        dim=1,
    )