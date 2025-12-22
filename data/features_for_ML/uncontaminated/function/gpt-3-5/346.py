def log_probs_from_logits_response_rmpad(input_ids, attention_mask, logits_rmpad, response_length):
    logits_rmpad = logits_rmpad[:response_length]
    logits_rmpad = logits_rmpad - logits_rmpad.max(axis=-1, keepdims=True)
    log_probs = logits_rmpad - np.log(np.sum(np.exp(logits_rmpad), axis=-1, keepdims=True))
    return log_probs