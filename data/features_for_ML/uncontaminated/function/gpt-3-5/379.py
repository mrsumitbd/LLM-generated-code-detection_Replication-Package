def pad_sequence_to_length(tensors, max_seq_len, pad_token_id, left_pad=False):
    padded_tensors = []
    for tensor in tensors:
        if left_pad:
            padded_tensor = [pad_token_id] * (max_seq_len - len(tensor)) + tensor[-max_seq_len:]
        else:
            padded_tensor = tensor[:max_seq_len] + [pad_token_id] * (max_seq_len - len(tensor))
        padded_tensors.append(padded_tensor)
    return padded_tensors