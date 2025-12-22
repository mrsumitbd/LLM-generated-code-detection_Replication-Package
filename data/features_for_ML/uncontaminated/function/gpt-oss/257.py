import torch

def convert_to_audio(multiframe, count):
    """
    Optimized version of convert_to_audio that eliminates inefficient tensor operations
    and reduces CPU-GPU transfers for much faster inference on high-end GPUs.

    Parameters
    ----------
    multiframe : torch.Tensor
        Tensor containing multiple frames of audio data. Expected shape:
        (batch, frames, channels) or (batch, frames, ...).
    count : int
        Number of frames to keep for the output audio.

    Returns
    -------
    torch.Tensor
        Audio waveform tensor of shape (batch, count * channels) or
        (batch, count, ...) depending on the input dimensionality.
    """
    # Ensure count does not exceed available frames
    frames = multiframe.shape[1]
    if count > frames:
        raise ValueError(f"Requested count {count} exceeds available frames {frames}")

    # Slice the desired number of frames
    sliced = multiframe[:, :count]

    # Flatten the remaining dimensions (except batch) into a single audio dimension
    # This keeps the operation on the GPU and avoids any CPU transfer.
    # If the input has more than 3 dimensions, we collapse all but batch.
    if sliced.ndim > 2:
        # Keep batch dimension, collapse the rest
        audio = sliced.reshape(sliced.shape[0], -1)
    else:
        # Already 2D: (batch, frames)
        audio = sliced

    return audio