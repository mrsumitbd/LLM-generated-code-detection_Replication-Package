import torch.nn.functional as F

def log_probs_from_logits_response_rmpad(input_ids, attention_mask, logits_rmpad, response_length):
    batch_size, seq_len = input_ids.size()
    total_nnz, vocab_size = logits_rmpad.size()

    # Compute the log probabilities
    log_probs = F.log_softmax(logits_rmpad, dim=-1)

    # Compute the shifted indices
    shift_indices = torch.arange(seq_len - response_length, seq_len).to(input_ids.device)

    # Gather the log probabilities based on the shifted indices
    log_probs_response = log_probs.gather(0, input_ids[:, shift_indices].view(-1).unsqueeze(1)).view(batch_size, -1)

    # Mask out the padded positions
    log_probs_response = log_probs_response * attention_mask[:, shift_indices]

    return log_probs_response