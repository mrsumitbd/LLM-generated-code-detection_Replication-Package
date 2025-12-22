import torch
import torch.nn.functional as F

def _hacked_flash_attention_forward(q, k, v, attn_mask=None, dropout_p=0.0):
    """
    Computes the forward pass of the Flash Attention operation.
    
    Args:
        q (torch.Tensor): The query tensor of shape (batch_size, num_heads, seq_len, head_dim).
        k (torch.Tensor): The key tensor of shape (batch_size, num_heads, seq_len, head_dim).
        v (torch.Tensor): The value tensor of shape (batch_size, num_heads, seq_len, head_dim).
        attn_mask (torch.Tensor, optional): The attention mask tensor of shape (batch_size, 1, seq_len, seq_len).
        dropout_p (float, optional): The dropout probability.
    
    Returns:
        torch.Tensor: The output tensor of shape (batch_size, num_heads, seq_len, head_dim).
    """
    batch_size, num_heads, seq_len, head_dim = q.shape
    
    # Compute the attention scores
    scores = torch.einsum('bhid,bhjd->bhij', q, k) / (head_dim ** 0.5)
    
    # Apply the attention mask
    if attn_mask is not None:
        scores = scores.masked_fill(attn_mask == 0, float('-inf'))
    
    # Compute the attention weights
    attn_weights = F.softmax(scores, dim=-1)
    
    # Apply dropout to the attention weights
    attn_weights = F.dropout(attn_weights, p=dropout_p, training=True)
    
    # Compute the output
    output = torch.einsum('bhij,bhjd->bhid', attn_weights, v)
    
    return output