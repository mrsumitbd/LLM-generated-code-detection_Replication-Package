import torch
import torch.nn as nn
import torch.nn.functional as F

class Attention_SDXL(nn.Module):
    def __init__(self, inner_dim, cross_attention_dim=None, num_heads=None, has_ipadapter=False, ipadp_scale=0.6, data_type=torch.float16):
        super(Attention_SDXL, self).__init__()
        self.inner_dim = inner_dim
        self.cross_attention_dim = cross_attention_dim if cross_attention_dim else inner_dim
        self.num_heads = num_heads if num_heads else 8
        self.has_ipadapter = has_ipadapter
        self.ipadp_scale = ipadp_scale
        self.data_type = data_type

        self.q_proj = nn.Linear(self.inner_dim, self.cross_attention_dim, bias=False)
        self.k_proj = nn.Linear(self.inner_dim, self.cross_attention_dim, bias=False)
        self.v_proj = nn.Linear(self.inner_dim, self.cross_attention_dim, bias=False)
        self.out_proj = nn.Linear(self.cross_attention_dim, self.inner_dim, bias=False)

        if self.has_ipadapter:
            self.ip_k = nn.Parameter(torch.zeros(self.num_heads, self.cross_attention_dim // self.num_heads), requires_grad=True)
            self.ip_v = nn.Parameter(torch.zeros(self.num_heads, self.cross_attention_dim // self.num_heads), requires_grad=True)

    def forward(self, hidden_states, encoder_hidden_states=None, batch=2, extra_options={}):
        q = self.q_proj(hidden_states)
        k = self.k_proj(encoder_hidden_states) if encoder_hidden_states is not None else self.k_proj(hidden_states)
        v = self.v_proj(encoder_hidden_states) if encoder_hidden_states is not None else self.v_proj(hidden_states)

        if self.has_ipadapter:
            q, k, v = self.update_ipkv(q, self.ip_k, self.ip_v, extra_options)

        attn_output = self.attention(q, k, v, batch, extra_options)
        output = self.out_proj(attn_output)
        return output

    def attention(self, q, k, v, batch, extra_options):
        q = q.view(batch, -1, self.num_heads, self.cross_attention_dim // self.num_heads).transpose(1, 2)
        k = k.view(batch, -1, self.num_heads, self.cross_attention_dim // self.num_heads).transpose(1, 2)
        v = v.view(batch, -1, self.num_heads, self.cross_attention_dim // self.num_heads).transpose(1, 2)

        attn_output = torch.matmul(q, k.transpose(-2, -1)) / (self.cross_attention_dim // self.num_heads) ** 0.5
        attn_output = F.softmax(attn_output, dim=-1)
        attn_output = torch.matmul(attn_output, v)
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch, -1, self.cross_attention_dim)
        return attn_output

    def update_scale_and_conuncon(self, q, ipadapter_kwargs, cond_or_uncond, block_type, t_idx):
        if self.has_ipadapter:
            q = self.update_ipkv(q, self.ip_k, self.ip_v, ipadapter_kwargs)
        return q

    def update_ipkv(self, weight, ip_k, ip_v, extra_options):
        if self.has_ipadapter:
            weight = weight.view(weight.size(0), self.num_heads, -1)
            weight[:, :, :] = weight[:, :, :] * (1 + self.ipadp_scale * ip_k) + self.ipadp_scale * ip_v
            weight = weight.view(weight.size(0), -1)
        return weight