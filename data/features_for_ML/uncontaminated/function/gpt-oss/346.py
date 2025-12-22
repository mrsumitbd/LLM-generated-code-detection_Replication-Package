import torch

def log_probs_from_logits_response_rmpad(input_ids, attention_mask, logits_rmpad, response_length):
    """
    Compute the log probabilities for the response tokens from logits that were
    produced on a padded‑removed (rmpad) input.  The logits are concatenated
    across the batch, so we need to map them back to the original positions.

    Args:
        input_ids (torch.LongTensor): [batch_size, seqlen]
        attention_mask (torch.LongTensor): [batch_size, seqlen] (1 for real tokens, 0 for pad)
        logits_rmpad (torch.FloatTensor): [total_nnz, vocab_size]  # total_nnz = sum(attention_mask)
        response_length (int): number of tokens in the response (from the end of each sequence)

    Returns:
        torch.FloatTensor: log probabilities for the response tokens,
                           shape [batch_size, response_length, vocab_size]
    """
    # Basic shapes
    batch_size, seqlen = input_ids.shape

    # Number of non‑pad tokens per batch
    non_pad_counts = attention_mask.sum(dim=1)  # [batch_size]

    # Offsets into the concatenated logits tensor
    # offsets[i] is the starting index for batch i in logits_rmpad
    offsets = torch.cat(
        [torch.tensor([0], device=non_pad_counts.device), non_pad_counts.cumsum(dim=0)[:-1]]
    )  # [batch_size]

    # Log‑softmax of all logits
    log_probs_all = torch.log_softmax(logits_rmpad, dim=-1)  # [total_nnz, vocab_size]

    # Prepare output list
    out = []

    for i in range(batch_size):
        start = offsets[i]
        end = start + non_pad_counts[i]

        # Indices of the response tokens in the concatenated logits
        resp_start = end - response_length
        resp_end = end

        # If the response starts before the first token (unlikely but safe)
        if resp_start < start:
            pad_len = start - resp_start
            # Pad with zeros (log‑prob of -inf is fine for log‑softmax)
            pad = torch.zeros((pad_len, logits_rmpad.size(1)),
                              device=log_probs_all.device,
                              dtype=log_probs_all.dtype)
            resp_log_probs = torch.cat([pad, log_probs_all[start:resp_end]], dim=0)
        else:
            resp_log_probs = log_probs_all[resp_start:resp_end]

        # Ensure the slice has exactly response_length rows
        if resp_log_probs.size(0) < response_length:
            pad_len = response_length - resp_log_probs.size(0)
            pad = torch.zeros((pad_len, logits_rmpad.size(1)),
                              device=log_probs_all.device,
                              dtype=log_probs_all.dtype)
            resp_log_probs = torch.cat([pad, resp_log_probs], dim=0)

        out.append(resp_log_probs)

    # Stack into [batch_size, response_length, vocab_size]
    return torch.stack(out, dim=0)