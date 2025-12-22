import torch

def apply_multimodal_rotary_pos_emb(q, k, cos, sin, mrope_section, unsqueeze_dim=1):
    batch_size, num_heads, seq_len, head_dim = q.shape
    
    # Split the channel dimension into temporal, height, and width sections
    q_temporal, q_height, q_width = torch.split(q, mrope_section, dim=-1)
    k_temporal, k_height, k_width = torch.split(k, mrope_section, dim=-1)
    
    # Apply rotary position embedding to each section
    q_temporal = (q_temporal * cos[:, :, :seq_len]) + (q_temporal * sin[:, :, :seq_len])
    q_height = (q_height * cos[:, :, :seq_len]) + (q_height * sin[:, :, :seq_len])
    q_width = (q_width * cos[:, :, :seq_len]) + (q_width * sin[:, :, :seq_len])
    
    k_temporal = (k_temporal * cos[:, :, :seq_len]) + (k_temporal * sin[:, :, :seq_len])
    k_height = (k_height * cos[:, :, :seq_len]) + (k_height * sin[:, :, :seq_len])
    k_width = (k_width * cos[:, :, :seq_len]) + (k_width * sin[:, :, :seq_len])
    
    # Concatenate the sections back together
    q = torch.cat([q_temporal, q_height, q_width], dim=-1)
    k = torch.cat([k_temporal, k_height, k_width], dim=-1)
    
    return q, k