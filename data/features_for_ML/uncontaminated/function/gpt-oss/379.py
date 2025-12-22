import torch

def pad_sequence_to_length(tensors, max_seq_len, pad_token_id, left_pad=False):
    """
    Pad a 2D tensor (e.g., responses, logprobs) in the last dimension to `max_seq_len`.

    Parameters
    ----------
    tensors : torch.Tensor
        Input tensor of shape [batch_size, seq_length].
    max_seq_len : int
        Desired sequence length after padding.
    pad_token_id : int or float
        Value to use for padding.
    left_pad : bool, optional
        If True, pad on the left side; otherwise pad on the right.

    Returns
    -------
    torch.Tensor
        Padded tensor of shape [batch_size, max_seq_len].
    """
    if not isinstance(tensors, torch.Tensor):
        raise TypeError("`tensors` must be a torch.Tensor")

    batch_size, seq_len = tensors.shape

    # If the sequence is already longer than or equal to the target length,
    # simply truncate it.
    if seq_len >= max_seq_len:
        return tensors[:, :max_seq_len]

    pad_len = max_seq_len - seq_len

    # Create a new tensor filled with the padding value.
    padded = torch.full(
        (batch_size, max_seq_len),
        pad_token_id,
        dtype=tensors.dtype,
        device=tensors.device,
    )

    if left_pad:
        # Place the original tensor at the end of the padded tensor.
        padded[:, pad_len:] = tensors
    else:
        # Place the original tensor at the beginning of the padded tensor.
        padded[:, :seq_len] = tensors

    return padded