def apply_multimodal_rotary_pos_emb(q, k, cos, sin, mrope_section, unsqueeze_dim=1):
    """Applies Rotary Position Embedding with Multimodal Sections to the query and key tensors (https://qwenlm.github.io/blog/qwen2-vl/).

    Explanation:
        Multimodal 3D rotary position embedding is an extension to 1D rotary position embedding. The input embedding
        sequence contains vision (images / videos) embedding and text embedding or just contains text embedding. For
        vision embedding part, we apply rotary position embedding on temporal, height and width dimension seperately.
        Here we split the channel dimension to 3 chunks for the temporal, height and width rotary position embedding.
        For text embedding part, we just apply 1D rotary position embedding. The three rotary position index (temporal,
        height and width) of text embedding is always the same, so the text embedding rotary position embedding has no
        difference with modern LLMs.

    Args:
        q (`torch.Tensor`): The query tensor.
        k (`torch.Tensor`): The key tensor.
        cos (`torch.Tensor`): The cosine part of the rotary embedding.
        sin (`torch.Tensor`): The sine part of the rotary embedding.
        position_ids (`torch.Tensor`):
            The position indices of the tokens corresponding to the query and key tensors. For example, this can be
            used to pass offsetted position ids when working with a KV-cache.
        mrope_section(`List(int)`):
            Multimodal rope section is for channel dimension of temporal, height and width in rope calculation.
        unsqueeze_dim (`int`, *optional*, defaults to 1):
            The 'unsqueeze_dim' argument specifies the dimension along which to unsqueeze cos[position_ids] and
            sin[position_ids] so that they can be properly broadcasted to the dimensions of q and k. For example, note
            that cos[position_ids] and sin[position_ids] have the shape [batch_size, seq_len, head_dim]. Then, if q and
            k have the shape [batch_size, heads, seq_len, head_dim], then setting unsqueeze_dim=1 makes
            cos[position_ids] and sin[position_ids] broadcastable to the shapes of q and k. Similarly, if q and k have
            the shape [batch_size, seq_len, heads, head_dim], then set unsqueeze_dim=2.
    Returns:
        `tuple(torch.Tensor)` comprising of the query and key tensors rotated using the Rotary Position Embedding.
    """
    import torch
    
    # Get the head dimension
    head_dim = q.shape[-1]
    
    # Split the head dimension into sections for temporal, height, width
    # mrope_section contains the sizes for each dimension
    sections = mrope_section + [head_dim - sum(mrope_section)]
    
    # Split q and k along the last dimension
    q_sections = torch.split(q, sections, dim=-1)
    k_sections = torch.split(k, sections, dim=-1)
    
    # Split cos and sin along the last dimension
    cos_sections = torch.split(cos, sections, dim=-1)
    sin_sections = torch.split(sin, sections, dim=-1)
    
    # Apply rotary embedding to each section
    q_rotated_sections = []
    k_rotated_sections = []
    
    for i, (q_sec, k_sec, cos_sec, sin_sec) in enumerate(zip(q_sections, k_sections, cos_sections, sin_sections)):
        # Unsqueeze cos and sin for broadcasting
        cos_sec = cos_sec.unsqueeze(unsqueeze_dim)
        sin_sec = sin_sec.unsqueeze(unsqueeze_dim)
        
        # Apply rotary embedding: (x * cos - y * sin, x * sin + y * cos)
        # where x and y are the real and imaginary parts
        # For a complex number representation: z = x + iy
        # Rotation: z' = z * e^(i*theta) = (x + iy) * (cos(theta) + i*sin(theta))
        
        # Split into pairs for complex number rotation
        q_sec_rot = (q_sec * cos_sec) + (
            torch.cat([-q_sec[..., q_sec.shape[-1]//2:], q_sec[..., :q_sec.shape[-1]//2]], dim=-1) * sin_sec
        )
        k_sec_rot = (k_sec * cos_sec) + (
            torch.cat([-k_sec[..., k_sec.shape[-1]//2:], k_sec[..., :k_sec.shape[-1]//2]], dim=-1) * sin_sec
        )
        
        q_rotated_sections.append(q_sec_rot)
        k_rotated_sections.append(k_sec_rot)
    
    # Concatenate all sections back together
    q_rotated = torch.cat(q_rotated_sections, dim=-1)
    k_rotated = torch.cat(k_rotated_sections, dim=-1)
    
    return q_rotated, k_rotated