def log_probs_from_logits_response_rmpad(input_ids, attention_mask, logits_rmpad, response_length):
    """Compute the log_probs from logits with rmpad logits and pad input. Note that
    logits_rmpad = model(input_ids_rmpad). For each sentences, there is a shift between
    logits and input_ids.
    The reason for this function to is to compute logprobs_from_logits in rmpad mode because it is memory-intensive
    for large vocab_size
    
    Args:
        input_ids: [batch_size, seqlen]
        attention_mask: [batch_size, seqlen]
        logits_rmpad: [total_nnz, vocab_size]
        response_length: int
    """
    import torch
    import torch.nn.functional as F
    
    batch_size, seqlen = input_ids.shape
    
    # Compute log softmax from logits
    log_probs_rmpad = F.log_softmax(logits_rmpad, dim=-1)
    
    # Create a mask for response tokens (last response_length tokens)
    response_mask = torch.zeros_like(attention_mask, dtype=torch.bool)
    response_mask[:, -response_length:] = attention_mask[:, -response_length:]
    
    # Flatten attention mask and response mask
    flat_attention_mask = attention_mask.view(-1)
    flat_response_mask = response_mask.view(-1)
    
    # Get indices where attention_mask is 1 (non-padded tokens)
    valid_indices = torch.where(flat_attention_mask == 1)[0]
    
    # Get indices where response_mask is 1 (response tokens)
    response_indices = torch.where(flat_response_mask == 1)[0]
    
    # Map response indices to rmpad indices
    # For each response index, find its position in the valid_indices
    response_rmpad_indices = []
    for resp_idx in response_indices:
        # Find position of resp_idx in valid_indices
        pos = torch.where(valid_indices == resp_idx)[0]
        if len(pos) > 0:
            response_rmpad_indices.append(pos[0].item())
    
    response_rmpad_indices = torch.tensor(response_rmpad_indices, device=input_ids.device)
    
    # Get the input_ids for response tokens (shifted by 1 for next token prediction)
    flat_input_ids = input_ids.view(-1)
    response_input_ids = flat_input_ids[response_indices]
    
    # Get log probs for the actual next tokens
    selected_log_probs = log_probs_rmpad[response_rmpad_indices, response_input_ids]
    
    # Reshape back to [batch_size, response_length]
    log_probs = torch.full((batch_size, seqlen), float('-inf'), device=input_ids.device)
    log_probs[response_mask] = selected_log_probs
    
    return log_probs