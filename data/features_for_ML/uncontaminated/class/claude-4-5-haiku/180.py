import torch
import torch.nn as nn
import torch.nn.functional as F
from einops import rearrange

class Attention_SDXL:

    def __init__(self, inner_dim, cross_attention_dim=None, num_heads=None, has_ipadapter=False, ipadp_scale=0.6, data_type=torch.float16):
        self.inner_dim = inner_dim
        self.cross_attention_dim = cross_attention_dim
        self.num_heads = num_heads if num_heads is not None else 8
        self.head_dim = inner_dim // self.num_heads
        self.has_ipadapter = has_ipadapter
        self.ipadp_scale = ipadp_scale
        self.data_type = data_type
        
        self.to_q = nn.Linear(inner_dim, inner_dim, bias=False)
        self.to_k = nn.Linear(cross_attention_dim or inner_dim, inner_dim, bias=False)
        self.to_v = nn.Linear(cross_attention_dim or inner_dim, inner_dim, bias=False)
        self.to_out = nn.Linear(inner_dim, inner_dim, bias=False)
        
        if self.has_ipadapter:
            self.ip_k_proj = nn.Linear(cross_attention_dim or inner_dim, inner_dim, bias=False)
            self.ip_v_proj = nn.Linear(cross_attention_dim or inner_dim, inner_dim, bias=False)
        
        self.scale = self.head_dim ** -0.5

    def forward(self, hidden_states, encoder_hidden_states=None, batch=2, extra_options={}):
        batch_size = hidden_states.shape[0]
        seq_len = hidden_states.shape[1]
        
        q = self.to_q(hidden_states)
        k = self.to_k(encoder_hidden_states if encoder_hidden_states is not None else hidden_states)
        v = self.to_v(encoder_hidden_states if encoder_hidden_states is not None else hidden_states)
        
        q = rearrange(q, 'b n (h d) -> b h n d', h=self.num_heads)
        k = rearrange(k, 'b n (h d) -> b h n d', h=self.num_heads)
        v = rearrange(v, 'b n (h d) -> b h n d', h=self.num_heads)
        
        sim = torch.einsum('b h i d, b h j d -> b h i j', q, k) * self.scale
        
        ipadapter_kwargs = extra_options.get('ipadapter_kwargs', {})
        cond_or_uncond = extra_options.get('cond_or_uncond', None)
        block_type = extra_options.get('block_type', None)
        t_idx = extra_options.get('t_idx', 0)
        
        if self.has_ipadapter and ipadapter_kwargs:
            ip_hidden_states = ipadapter_kwargs.get('ip_hidden_states', None)
            if ip_hidden_states is not None:
                ip_k = self.ip_k_proj(ip_hidden_states)
                ip_v = self.ip_v_proj(ip_hidden_states)
                
                ip_k = rearrange(ip_k, 'b n (h d) -> b h n d', h=self.num_heads)
                ip_v = rearrange(ip_v, 'b n (h d) -> b h n d', h=self.num_heads)
                
                weight = self.update_scale_and_conuncon(q, ipadapter_kwargs, cond_or_uncond, block_type, t_idx)
                ip_k, ip_v = self.update_ipkv(weight, ip_k, ip_v, extra_options)
                
                ip_sim = torch.einsum('b h i d, b h j d -> b h i j', q, ip_k) * self.scale
                sim = sim + ip_sim * self.ipadp_scale
        
        attn = F.softmax(sim, dim=-1)
        out = torch.einsum('b h i j, b h j d -> b h i d', attn, v)
        out = rearrange(out, 'b h n d -> b n (h d)')
        out = self.to_out(out)
        
        return out

    def update_scale_and_conuncon(self, q, ipadapter_kwargs, cond_or_uncond, block_type, t_idx):
        weight = ipadapter_kwargs.get('weight', self.ipadp_scale)
        
        if cond_or_uncond is not None:
            if cond_or_uncond == 'uncond':
                weight = weight * 0.5
        
        if block_type is not None:
            if block_type == 'down':
                weight = weight * 0.8
            elif block_type == 'mid':
                weight = weight * 1.0
            elif block_type == 'up':
                weight = weight * 0.9
        
        if t_idx is not None:
            weight = weight * (1.0 - t_idx * 0.1)
        
        return weight

    def update_ipkv(self, weight, ip_k, ip_v, extra_options):
        scale_factor = weight
        
        ip_k = ip_k * scale_factor
        ip_v = ip_v * scale_factor
        
        return ip_k, ip_v