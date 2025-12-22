import torch
from typing import Optional, Tuple, List

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
) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[List[torch.Tensor]]]:
    """
    Forward pass for a chunked gated delta rule attention.

    Parameters
    ----------
    q, k, v : torch.Tensor
        Query, key, and value tensors of shape
        (batch, seq_len, heads, dim_k).
    g : torch.Tensor
        Gating tensor of the same shape as `q`.
    beta : torch.Tensor
        Decay tensor of shape (batch, heads, dim_k) or broadcastable.
    scale : float
        Scaling factor for the dot‑product.
    initial_state : Optional[torch.Tensor]
        Initial state tensor of shape (batch, heads, dim_k) or broadcastable.
    output_final_state : bool
        If True, return the final state after processing all chunks.
    cu_seqlens : Optional[torch.IntTensor]
        Cumulative sequence lengths for each batch element. If None,
        the entire sequence is processed as a single chunk.
    return_chunked_states : bool
        If True, also return a list of intermediate states for each chunk.

    Returns
    -------
    output : torch.Tensor
        The attention output of shape (batch, seq_len, heads, dim_k).
    final_state : Optional[torch.Tensor]
        The final state if `output_final_state` is True, otherwise None.
    chunked_states : Optional[List[torch.Tensor]]
        List of intermediate states per chunk if `return_chunked_states` is True,
        otherwise None.
    """
    # Ensure tensors are contiguous for efficient indexing
    q = q.contiguous()
    k = k.contiguous()
    v = v.contiguous()
    g = g.contiguous()
    beta = beta.contiguous()

    batch, seq_len, heads, dim_k = q.shape

    # Prepare output tensor
    output = torch.empty_like(q)

    # Prepare state tensors
    if initial_state is None:
        state = torch.zeros(batch, heads, dim_k, dtype=q.dtype, device=q.device)
    else:
        state = initial_state.contiguous()

    # List to store chunked states if requested
    chunked_states: List[torch.Tensor] = []

    # Helper to process a single chunk
    def _process_chunk(start: int, end: int, batch_idx: int):
        nonlocal state
        q_chunk = q[batch_idx, start:end]          # (chunk_len, heads, dim_k)
        k_chunk = k[batch_idx, start:end]          # (chunk_len, heads, dim_k)
        v_chunk = v[batch_idx, start:end]          # (chunk_len, heads, dim_k)
        g_chunk = g[batch_idx, start:end]          # (chunk_len, heads, dim_k)

        # Compute attention scores
        # (chunk_len, heads, dim_k) @ (chunk_len, heads, dim_k).transpose(-2,-1)
        # -> (chunk_len, heads, chunk_len)
        scores = torch.einsum("bhd,bhd->bh", q_chunk, k_chunk)  # wrong shape
        # Actually we need dot product across dim_k for each head
        # Use einsum: (bhd) @ (bhd) -> (bh)
        # But we need matrix multiplication: (chunk_len, heads, dim_k) @ (chunk_len, heads, dim_k).transpose(-2,-1)
        # We can reshape to (chunk_len, heads, dim_k) -> (chunk_len, heads, dim_k)
        # Use torch.einsum: "bhd,bhd->bh" gives scalar per head, not correct.
        # Instead, we compute per head: for each head, compute q_chunk[:,h,:] @ k_chunk[:,h,:].transpose(-1,-2)
        # Use torch.einsum: "bhd,bhd->bh" is wrong. Let's do:
        scores = torch.einsum("bhd,bhd->bh", q_chunk, k_chunk)  # still wrong
        # Actually we need (chunk_len, heads, dim_k) @ (chunk_len, heads, dim_k).transpose(-2,-1)
        # We can use torch.einsum: "bhd,bhd->bh" gives sum over dim_k, not matrix.
        # Let's compute using torch.matmul after permuting:
        q_perm = q_chunk.permute(1, 0, 2)  # (heads, chunk_len, dim_k)
        k_perm = k_chunk.permute(1, 0, 2)  # (heads, chunk_len, dim_k)
        # Compute scores per head: (heads, chunk_len, dim_k) @ (heads, dim_k, chunk_len)
        scores = torch.matmul(q_perm, k_perm.transpose(-2, -1))  # (heads, chunk_len, chunk_len)
        scores = scores * scale
        # Softmax over last dimension
        attn = torch.softmax(scores, dim=-1)  # (heads, chunk_len, chunk_len)
        # Multiply by v
        v_perm = v_chunk.permute(1, 0, 2)  # (heads, chunk_len, dim_k)
        attn_out = torch.matmul(attn, v_perm)  # (heads, chunk_len, dim_k)
        attn_out = attn_out.permute(1, 0, 2)  # (chunk_len, heads, dim_k)

        # Apply gating
        gated = g_chunk * attn_out  # (chunk_len, heads, dim_k)

        # Update state
        # state shape: (batch, heads, dim_k)
        # For this batch_idx, update state
        state[batch_idx] = beta[batch_idx] * state[batch_idx] + gated.sum(dim=0)

        # Write output
        output[batch_idx, start:end] = gated

        # Store chunked state if requested
        if return_chunked_states:
            chunked_states.append(state[batch_idx].clone())

    # If cu_seqlens provided, use it to split into chunks
    if cu_seqlens is not None:
        # cu_seqlens shape: (batch + 1,)
        # For each batch element, process chunks defined by cu_seqlens
        for b in range(batch):
            start = cu_seqlens[b].item()
            end = cu_seqlens[b + 1].item()
            _process_chunk(start, end, b)
    else:
        # Single chunk for each batch element
        for b in range(batch):
            _process_chunk(0, seq_len, b)

    final_state = state if output_final_state else None
    chunked_states_out = chunked_states if return_chunked_states else None

    return output, final_state, chunked_states_out