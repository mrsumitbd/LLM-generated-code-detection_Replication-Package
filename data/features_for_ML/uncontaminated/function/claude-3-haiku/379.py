def pad_sequence_to_length(tensors, max_seq_len, pad_token_id, left_pad=False):
    """
    pad a 2D tensors (e.g. responses, logprobs) in the last dim to max_seq_length.
    input shape: [bs, seq_length]
    output shape: [bs, max_seq_length]
    (0, max_seq_len - tensors.shape[-1]) means right pad to max_seq_length and no left pad
    """
    batch_size = tensors.shape[0]
    seq_length = tensors.shape[1]
    pad_size = max_seq_len - seq_length

    if left_pad:
        pad_tensor = torch.full((batch_size, pad_size), pad_token_id, dtype=tensors.dtype, device=tensors.device)
        return torch.cat([pad_tensor, tensors], dim=-1)
    else:
        return torch.nn.functional.pad(tensors, (0, pad_size), value=pad_token_id)