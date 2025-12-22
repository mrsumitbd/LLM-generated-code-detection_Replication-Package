import torch
import torch.nn as nn
import torch.nn.functional as F


class Attention_SDXL(nn.Module):
    """
    A lightweight implementation of a self/cross attention block that optionally
    supports IPAdapter style conditioning.  The implementation is intentionally
    simple and focuses on the API required by the skeleton.
    """

    def __init__(
        self,
        inner_dim,
        cross_attention_dim=None,
        num_heads=None,
        has_ipadapter=False,
        ipadp_scale=0.6,
        data_type=torch.float16,
    ):
        super().__init__()
        self.inner_dim = inner_dim
        self.cross_attention_dim = cross_attention_dim or inner_dim
        self.num_heads = num_heads or 8
        self.has_ipadapter = has_ipadapter
        self.ipadp_scale = ipadp_scale
        self.data_type = data_type

        # Linear projections for query, key, value and output
        self.to_q = nn.Linear(inner_dim, inner_dim, bias=False)
        self.to_k = nn.Linear(inner_dim, inner_dim, bias=False)
        self.to_v = nn.Linear(inner_dim, inner_dim, bias=False)
        self.to_out = nn.Linear(inner_dim, inner_dim, bias=False)

        # Optional IPAdapter key/value projections
        if self.has_ipadapter:
            self.ip_k_proj = nn.Linear(inner_dim, inner_dim, bias=False)
            self.ip_v_proj = nn.Linear(inner_dim, inner_dim, bias=False)

        # Scaling factor for attention
        self.scale = (inner_dim // self.num_heads) ** -0.5

    def forward(self, hidden_states, encoder_hidden_states=None, batch=2, extra_options={}):
        """
        hidden_states: (B, N, C)
        encoder_hidden_states: (B, M, C) or None
        """
        B, N, C = hidden_states.shape

        # Query
        q = self.to_q(hidden_states)  # (B, N, C)

        # Key and Value
        if encoder_hidden_states is not None:
            k = self.to_k(encoder_hidden_states)  # cross-attention
            v = self.to_v(encoder_hidden_states)
            block_type = "cross"
        else:
            k = self.to_k(hidden_states)  # self-attention
            v = self.to_v(hidden_states)
            block_type = "self"

        # Optional IPAdapter conditioning
        if self.has_ipadapter:
            ip_k = self.ip_k_proj(hidden_states)
            ip_v = self.ip_v_proj(hidden_states)
            # Update IP key/value with optional scaling
            ip_k, ip_v = self.update_ipkv(self.ipadp_scale, ip_k, ip_v, extra_options)
            # Concatenate IP key/value to the original ones
            k = torch.cat([k, ip_k], dim=1)
            v = torch.cat([v, ip_v], dim=1)

        # Reshape for multi-head attention
        q = q.view(B, N, self.num_heads, C // self.num_heads).transpose(1, 2)  # (B, H, N, D)
        k = k.view(B, -1, self.num_heads, C // self.num_heads).transpose(1, 2)  # (B, H, M, D)
        v = v.view(B, -1, self.num_heads, C // self.num_heads).transpose(1, 2)  # (B, H, M, D)

        # Attention scores
        attn_weights = torch.matmul(q, k.transpose(-2, -1)) * self.scale  # (B, H, N, M)
        attn_weights = F.softmax(attn_weights, dim=-1)

        # Attention output
        attn_output = torch.matmul(attn_weights, v)  # (B, H, N, D)
        attn_output = attn_output.transpose(1, 2).contiguous().view(B, N, C)

        # Final projection
        out = self.to_out(attn_output)

        # Optional scaling for conditional/unconditional
        if "cond_or_uncond" in extra_options:
            out = self.update_scale_and_conuncon(
                out,
                ipadapter_kwargs=extra_options.get("ipadapter_kwargs", {}),
                cond_or_uncond=extra_options["cond_or_uncond"],
                block_type=block_type,
                t_idx=extra_options.get("t_idx", 0),
            )

        return out

    def update_scale_and_conuncon(self, q, ipadapter_kwargs, cond_or_uncond, block_type, t_idx):
        """
        Simple scaling logic:
        - If unconditional, scale by 0.5
        - If conditional, keep as is
        - Optionally apply a time‑dependent factor
        """
        scale = 1.0
        if cond_or_uncond == "uncond":
            scale = 0.5
        # Example time‑dependent scaling (optional)
        if t_idx is not None:
            scale *= 1.0 + 0.01 * t_idx
        return q * scale

    def update_ipkv(self, weight, ip_k, ip_v, extra_options):
        """
        Apply a weight to the IPAdapter key/value tensors.
        """
        ip_k = ip_k * weight
        ip_v = ip_v * weight
        return ip_k, ip_v