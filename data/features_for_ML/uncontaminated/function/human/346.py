import torch
import torch.distributed
from flash_attn.bert_padding import pad_input, unpad_input
from flash_attn.bert_padding import pad_input

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
    from flash_attn.bert_padding import pad_input, unpad_input

    batch_size, seqlen = input_ids.shape
    input_ids_rmpad, indices, *_ = unpad_input(input_ids.unsqueeze(-1), attention_mask=attention_mask)
    input_ids_rmpad = input_ids_rmpad.squeeze(-1)
    input_ids_rmpad_rolled = torch.roll(input_ids_rmpad, shifts=-1, dims=0)
    full_log_probs_rmpad = logprobs_from_logits(logits=logits_rmpad, labels=input_ids_rmpad_rolled)  # (total_nnz,)
    full_output = pad_input(hidden_states=full_log_probs_rmpad.unsqueeze(-1),
                            indices=indices,
                            batch=batch_size,
                            seqlen=seqlen)
    output = full_output.squeeze(-1)[:, -response_length - 1:-1]  # [batch_size, response_length]
    return output