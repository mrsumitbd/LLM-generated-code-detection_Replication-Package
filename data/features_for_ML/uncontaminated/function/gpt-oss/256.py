import torch
import itertools

def apply_multimodal_rotary_pos_emb(q, k, cos, sin, mrope_section, unsqueeze_dim=1):
    """
    Applies Rotary Position Embedding with Multimodal Sections to the query and key tensors.
    """
    # Helper to rotate half of the last dimension
    def rotate_half(x):
        # x shape (..., dim)
        dim = x.shape[-1]
        half = dim // 2
        # For odd dim, the last element is left unchanged
        if dim % 2 == 0:
            x1 = x[..., :half]
            x2 = x[..., half:]
            return torch.cat((x2, -x1), dim=-1)
        else:
            x1 = x[..., :half]
            x2 = x[..., half:-1]
            last = x[..., -1:]
            return torch.cat((x2, -x1, last), dim=-1)

    # Unsqueeze cos and sin to match q/k shape for broadcasting
    cos = cos.unsqueeze(unsqueeze_dim)
    sin = sin.unsqueeze(unsqueeze_dim)

    # Compute cumulative splits for channel dimension
    splits = [0] + list(itertools.accumulate(mrope_section))
    # Ensure splits cover the entire last dimension
    if splits[-1] != q.shape[-1]:
        raise ValueError("mrope_section does not match the channel dimension size")

    # Apply rotary to each chunk
    q_chunks = []
    k_chunks = []
    for i in range(len(mrope_section)):
        start = splits[i]
        end = splits[i + 1]
        q_chunk = q[..., start:end]
        k_chunk = k[..., start:end]
        cos_chunk = cos[..., start:end]
        sin_chunk = sin[..., start:end]

        q_rot = (q_chunk * cos_chunk) + (rotate_half(q_chunk) * sin_chunk)
        k_rot = (k_chunk * cos_chunk) + (rotate_half(k_chunk) * sin_chunk)

        q_chunks.append(q_rot)
        k_chunks.append(k_rot)

    # Concatenate back along the channel dimension
    q_out = torch.cat(q_chunks, dim=-1)
    k_out = torch.cat(k_chunks, dim=-1)

    return q_out, k_out