def pad_sequence_to_length(tensors, max_seq_len, pad_token_id, left_pad=False):
    """
    pad a 2D tensors (e.g. responses, logprobs) in the last dim to max_seq_length.
    input shape: [bs, seq_length]
    output shape: [bs, max_seq_length]
    (0, max_seq_len - tensors.shape[-1]) means right pad to max_seq_length and no left pad
    """
    import torch
    
    current_seq_len = tensors.shape[-1]
    
    if current_seq_len >= max_seq_len:
        return tensors
    
    pad_length = max_seq_len - current_seq_len
    
    if left_pad:
        # Left pad: (left_pad, right_pad)
        pad = (pad_length, 0)
    else:
        # Right pad: (left_pad, right_pad)
        pad = (0, pad_length)
    
    padded_tensors = torch.nn.functional.pad(tensors, pad, value=pad_token_id)
    
    return padded_tensors