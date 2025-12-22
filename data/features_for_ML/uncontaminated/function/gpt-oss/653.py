import math
import torch
import torch.nn.functional as F

def _hacked_flash_attention_forward(*args, **kwargs):
    """
    A lightweight fallback implementation of flash attention.
    It accepts the same arguments as the original flash attention
    implementation (query, key, value, attn_mask, dropout_p, is_causal, etc.)
    and performs a scaled dot‑product attention computation.

    Parameters
    ----------
    query : torch.Tensor
        Query tensor of shape (..., seq_len_q, head_dim).
    key : torch.Tensor
        Key tensor of shape (..., seq_len_k, head_dim).
    value : torch.Tensor
        Value tensor of shape (..., seq_len_v, head_dim).
    attn_mask : torch.Tensor, optional
        Mask tensor broadcastable to the attention matrix.
    dropout_p : float, optional
        Dropout probability applied to the attention weights.
    is_causal : bool, optional
        If True, applies a causal mask to prevent attention to future positions.
    training : bool, optional
        Whether to apply dropout (default: False).
    **kwargs : dict
        Additional keyword arguments are ignored.

    Returns
    -------
    torch.Tensor
        The result of the attention operation.
    """
    # Extract positional arguments
    if len(args) < 3:
        raise ValueError("Expected at least 3 positional arguments: query, key, value")
    query, key, value = args[:3]

    # Extract keyword arguments with defaults
    attn_mask = kwargs.get("attn_mask", None)
    dropout_p = kwargs.get("dropout_p", 0.0)
    is_causal = kwargs.get("is_causal", False)
    training = kwargs.get("training", False)

    # Compute scaled dot‑product attention
    d_k = query.size(-1)
    scale = 1.0 / math.sqrt(d_k)
    attn_scores = torch.matmul(query, key.transpose(-2, -1)) * scale

    # Apply causal mask if requested
    if is_causal:
        seq_len_q = attn_scores.size(-2)
        seq_len_k = attn_scores.size(-1)
        causal_mask = torch.triu(
            torch.ones((seq_len_q, seq_len_k), dtype=attn_scores.dtype, device=attn_scores.device),
            diagonal=1,
        ).bool()
        attn_scores = attn_scores.masked_fill(causal_mask, float("-inf"))

    # Apply external attention mask if provided
    if attn_mask is not None:
        if attn_mask.dtype == torch.bool:
            attn_scores = attn_scores.masked_fill(attn_mask, float("-inf"))
        else:
            attn_scores = attn_scores + attn_mask

    # Softmax to obtain attention probabilities
    attn_weights = F.softmax(attn_scores, dim=-1)

    # Apply dropout if requested
    if dropout_p > 0.0 and training:
        attn_weights = F.dropout(attn_weights, p=dropout_p, training=training)

    # Compute the weighted sum of values
    output = torch.matmul(attn_weights, value)
    return output