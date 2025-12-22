import torch

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
    batch_size, seq_len, head_dim = q.shape
    device = q.device

    if initial_state is None:
        state = torch.zeros(batch_size, head_dim, device=device)
    else:
        state = initial_state

    output = torch.zeros(batch_size, seq_len, head_dim, device=device)
    chunked_states = []

    if cu_seqlens is None:
        cu_seqlens = torch.arange(0, (batch_size + 1) * seq_len, step=seq_len, dtype=torch.int32, device=device)

    for i in range(seq_len):
        q_t = q[:, i, :]
        k_t = k[:, i, :]
        v_t = v[:, i, :]
        g_t = g[:, i, :]

        state = state + scale * (q_t * k_t - state) * g_t
        state = state * (1 - beta) + beta * state
        output[:, i, :] = state

        if return_chunked_states:
            chunked_states.append(state.clone())

    if output_final_state:
        return output, state
    elif return_chunked_states:
        return output, chunked_states
    else:
        return output