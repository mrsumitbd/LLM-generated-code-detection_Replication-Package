import torch
from typing import Optional

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
    if initial_state is None:
        state = torch.zeros_like(q)
    else:
        state = initial_state

    if cu_seqlens is not None:
        cu_seqlens = cu_seqlens.cpu().numpy()

    chunked_states = []
    for i in range(q.size(1)):
        q_i = q[:, i]
        k_i = k[:, i]
        v_i = v[:, i]
        g_i = g[:, i]
        beta_i = beta[:, i]

        state = state + scale * (q_i - state) * g_i
        state = state + scale * (v_i - state) * (1 - g_i) * beta_i

        if cu_seqlens is not None:
            state = state * (1 - cu_seqlens[i])

        chunked_states.append(state.unsqueeze(1))

    if output_final_state:
        final_state = state
    else:
        final_state = None

    if return_chunked_states:
        return torch.cat(chunked_states, dim=1), final_state
    else:
        return final_state