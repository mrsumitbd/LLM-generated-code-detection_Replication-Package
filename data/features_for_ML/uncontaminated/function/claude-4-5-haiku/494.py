def chunk_gated_delta_rule_fwd(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    g: torch.Tensor,
    beta: torch.Tensor,
    scale: float,
    initial_state: Optional[torch.Tensor],
    output_final_state: bool,
    cu_seqlens: Optional[torch.IntTensor] = None,
    return_chunked_states: bool = False,
):
    """
    Forward pass for chunk-wise gated delta rule attention.
    
    Args:
        q: Query tensor of shape (batch_size * seq_len, num_heads, head_dim)
        k: Key tensor of shape (batch_size * seq_len, num_heads, head_dim)
        v: Value tensor of shape (batch_size * seq_len, num_heads, head_dim)
        g: Gate tensor of shape (batch_size * seq_len, num_heads, 1)
        beta: Beta tensor of shape (batch_size * seq_len, num_heads, 1)
        scale: Scaling factor for attention scores
        initial_state: Optional initial state for recurrence
        output_final_state: Whether to output the final state
        cu_seqlens: Cumulative sequence lengths for variable length sequences
        return_chunked_states: Whether to return intermediate chunk states
    
    Returns:
        Tuple containing output and optionally final state and chunked states
    """
    batch_size_seq, num_heads, head_dim = q.shape
    device = q.device
    dtype = q.dtype
    
    # Handle sequence lengths
    if cu_seqlens is None:
        cu_seqlens = torch.tensor([0, batch_size_seq], device=device, dtype=torch.int32)
    
    num_sequences = cu_seqlens.shape[0] - 1
    
    # Initialize output
    output = torch.zeros_like(v)
    
    # Initialize state for recurrence
    if initial_state is None:
        state = torch.zeros(num_sequences, num_heads, head_dim, head_dim, device=device, dtype=dtype)
    else:
        state = initial_state.clone()
    
    chunked_states = [] if return_chunked_states else None
    
    # Process each sequence
    for seq_idx in range(num_sequences):
        start_idx = cu_seqlens[seq_idx].item()
        end_idx = cu_seqlens[seq_idx + 1].item()
        seq_len = end_idx - start_idx
        
        # Extract sequence data
        q_seq = q[start_idx:end_idx]  # (seq_len, num_heads, head_dim)
        k_seq = k[start_idx:end_idx]  # (seq_len, num_heads, head_dim)
        v_seq = v[start_idx:end_idx]  # (seq_len, num_heads, head_dim)
        g_seq = g[start_idx:end_idx]  # (seq_len, num_heads, 1)
        beta_seq = beta[start_idx:end_idx]  # (seq_len, num_heads, 1)
        
        # Current state for this sequence
        current_state = state[seq_idx]  # (num_heads, head_dim, head_dim)
        
        # Process sequence position by position
        for pos in range(seq_len):
            q_pos = q_seq[pos]  # (num_heads, head_dim)
            k_pos = k_seq[pos]  # (num_heads, head_dim)
            v_pos = v_seq[pos]  # (num_heads, head_dim)
            g_pos = g_seq[pos]  # (num_heads, 1)
            beta_pos = beta_seq[pos]  # (num_heads, 1)
            
            # Compute attention scores: (num_heads, head_dim) @ (num_heads, head_dim, head_dim)
            # Result: (num_heads, head_dim)
            scores = torch.einsum('hd,hde->he', q_pos, current_state) * scale
            
            # Apply gating and beta
            # scores: (num_heads, head_dim)
            # v_pos: (num_heads, head_dim)
            out_pos = g_pos * torch.sigmoid(beta_pos) * torch.sum(scores * v_pos, dim=-1, keepdim=True)
            
            # Update state with delta rule
            # current_state: (num_heads, head_dim, head_dim)
            # k_pos: (num_heads, head_dim)
            # v_pos: (num_heads, head_dim)
            delta = torch.einsum('hd,he->hde', k_pos, v_pos)
            current_state = current_state + delta
            
            output[start_idx + pos] = out_pos.squeeze(-1)
        
        # Store final state
        state[seq_idx] = current_state
        
        if return_chunked_states:
            chunked_states.append(current_state.clone())
    
    # Prepare return values
    result = [output]
    
    if output_final_state:
        result.append(state)
    
    if return_chunked_states:
        result.append(torch.stack(chunked_states))
    
    return tuple(result) if len(result) > 1 else result[0]