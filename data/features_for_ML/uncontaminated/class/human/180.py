import torch
from fastdm.layer.qlinear import QLinear
from fastdm.kernel.operators_set import scaled_dot_product_attention, gelu_and_mul

class Attention_SDXL:
    def __init__(self, inner_dim, cross_attention_dim=None, num_heads=None, has_ipadapter = False, ipadp_scale = 0.6, data_type = torch.float16):
        super(Attention_SDXL, self).__init__()

        self.inner_dim = inner_dim

        if num_heads is None:
            self.head_dim = 64
            self.num_heads = inner_dim // self.head_dim
        else:
            self.num_heads = num_heads
            self.head_dim = inner_dim // num_heads

        self.scale = self.head_dim**-0.5
        self.has_ipadapter = has_ipadapter
        self.ipadp_scale = ipadp_scale if has_ipadapter else None

        # if cross_attention_dim is None:
        #     cross_attention_dim = inner_dim

        if cross_attention_dim is None: #attn1
            self.qkv_proj = QLinear(inner_dim, inner_dim*3, bias=False, data_type=data_type)
        else: #attn2
            self.q_proj = QLinear(inner_dim, inner_dim, bias=False, data_type=data_type)
            self.kv_proj = QLinear(cross_attention_dim, inner_dim*2, bias=False, data_type=data_type)

        if self.has_ipadapter:
            self.ipadp_kv_proj = QLinear(cross_attention_dim, inner_dim*2, data_type=data_type)

        self.out_proj = QLinear(inner_dim, inner_dim, data_type=data_type)

    def forward(self, hidden_states, encoder_hidden_states=None, batch=2, extra_options= {}):

        # if self.qkv_weight is not None:
        if hasattr(self, "qkv_proj"):
            qkv_out = self.qkv_proj.forward(hidden_states)
            q = qkv_out[:,0:self.inner_dim].view(batch, -1, self.inner_dim)
            k = qkv_out[:,self.inner_dim:(2*self.inner_dim)].view(batch, -1, self.inner_dim)
            v = qkv_out[:,(2*self.inner_dim):(3*self.inner_dim)].view(batch, -1, self.inner_dim)

        else: #attn2
            if self.has_ipadapter and isinstance(encoder_hidden_states, tuple):
                encoder_hidden_states, ip_hidden_states, ip_neg_hidden_states = encoder_hidden_states

            q = self.q_proj.forward(hidden_states).view(batch, -1, self.inner_dim)
            kv_out = (
                    self.kv_proj.forward(encoder_hidden_states.view(encoder_hidden_states.shape[0]*encoder_hidden_states.shape[1], encoder_hidden_states.shape[2]))
                    if encoder_hidden_states is not None
                    else self.kv_proj.forward(hidden_states)
            )
            k = kv_out[:,0:self.inner_dim].view(batch, -1, self.inner_dim)
            v = kv_out[:,self.inner_dim:(2*self.inner_dim)].view(batch, -1, self.inner_dim)
        
            # comfyui ipadapter patch kwargs, if it is None, current block not compute ipadapter
            ipadapter_kwargs = extra_options.get("ipadapter_kwargs", None)

            if self.has_ipadapter:
                # for diffusers and comfyui ipadapter, there is 3 cases:
                # 1) diffusers: ipadapter_kwargs is None and extra_options is empty
                # 2) comfyui compute ipadapter: ipadapter_kwargs is not None and sigmas is in [sigmas_start, sigmas_end]
                # 3) comfyui not compute ipadapter: ipadapter_kwargs is None and extra_options is not empty
                def compute_kv(hidden_states):
                    kv_out = self.ipadp_kv_proj.forward(hidden_states[0])
                    k = kv_out[:, 0:self.inner_dim].view(batch, -1, self.inner_dim)
                    v = kv_out[:, self.inner_dim:(2 * self.inner_dim)].view(batch, -1, self.inner_dim)
                    return k, v
            
                if ipadapter_kwargs is None and not extra_options: # 1)diffusers
                    ipadp_k, ipadp_v = compute_kv(ip_hidden_states)
                    if ip_neg_hidden_states is not None:
                        ipadp_neg_k, ipadp_neg_v = compute_kv(ip_neg_hidden_states)

                        ip_k = torch.cat([ipadp_neg_k, ipadp_k], dim=0).view(batch, -1, self.inner_dim)
                        ip_v = torch.cat([ipadp_neg_v, ipadp_v], dim=0).view(batch, -1, self.inner_dim)
                    else:
                        ip_k = ipadp_k
                        ip_v = ipadp_v
                elif ipadapter_kwargs is not None: # 2) comfyui compute ipadapter
                    sigma = extra_options["sigmas"].detach().cpu()[0].item() if 'sigmas' in extra_options else 999999999.9
                    sigma_right = sigma <= ipadapter_kwargs[0]["sigma_start"] and sigma >= ipadapter_kwargs[0]["sigma_end"]
                    if sigma_right:
                        # for comfyui ipadapter, update ipadp scale and get ip_hidden_states, ip_neg_hidden_states from extra_options
                        self.ipadp_scale,ip_hidden_states,ip_neg_hidden_states = self.update_scale_and_conuncon(q, 
                                                                                                                ipadapter_kwargs, 
                                                                                                                extra_options["cond_or_uncond"], 
                                                                                                                extra_options["block"][0], 
                                                                                                                extra_options["transformer_index"])

                        ipadp_k, ipadp_v = compute_kv(ip_hidden_states)
                        if ip_neg_hidden_states is not None:
                            ipadp_neg_k, ipadp_neg_v = compute_kv(ip_neg_hidden_states)

                            ip_k = torch.cat([ipadp_neg_k, ipadp_k], dim=0).view(batch, -1, self.inner_dim)
                            ip_v = torch.cat([ipadp_neg_v, ipadp_v], dim=0).view(batch, -1, self.inner_dim)
                        else:
                            ip_k = ipadp_k
                            ip_v = ipadp_v
                        
                        # for comfyui ipadapter, update k v according to embeds_scaling, support['K+mean(V) w/ C penalty','K+V w/ C penalty','K+V' ]
                        embeds_scaling, ip_k, ip_v = self.update_ipkv(self.ipadp_scale, ip_k, ip_v, extra_options)

        attn_output = scaled_dot_product_attention(q, k, v, self.num_heads, self.num_heads, self.head_dim, scale=self.scale)

        if self.has_ipadapter:
            # there are 3 cases same as above
            tmp_attn_out = scaled_dot_product_attention(q, ip_k, ip_v, self.num_heads, self.num_heads, self.head_dim, scale=self.scale)
            if ipadapter_kwargs is None and not extra_options:
                attn_output = attn_output + self.ipadp_scale * tmp_attn_out
            elif ipadapter_kwargs is not None:
                if sigma_right:
                    ip_attn_output = self.ipadp_scale * tmp_attn_out if embeds_scaling == "V only" else tmp_attn_out
                    attn_output = attn_output + ip_attn_output
        attn_output = attn_output.view(-1, self.inner_dim)
        attn_output = self.out_proj.forward(attn_output)

        return attn_output
    
    def update_scale_and_conuncon(self, q, ipadapter_kwargs,cond_or_uncond, block_type, t_idx):
        # update ipadapter scale according node weight
        cond_alt = None
        ipadapter = ipadapter_kwargs[0]["ipadapter"]
        weight = ipadapter_kwargs[0]["weight"]
        weight_type = ipadapter_kwargs[0]["weight_type"]
        cond = ipadapter_kwargs[0]["cond"]
        uncond = ipadapter_kwargs[0]["uncond"]

        layers = 11 if '101_to_k_ip' in ipadapter.ip_layers.to_kvs else 16
        b = q.shape[0]

        if weight_type == 'ease in':
            weight = weight * (0.05 + 0.95 * (1 - t_idx / layers))
        elif weight_type == 'ease out':
            weight = weight * (0.05 + 0.95 * (t_idx / layers))
        elif weight_type == 'ease in-out':
            weight = weight * (0.05 + 0.95 * (1 - abs(t_idx - (layers/2)) / (layers/2)))
        elif weight_type == 'reverse in-out':
            weight = weight * (0.05 + 0.95 * (abs(t_idx - (layers/2)) / (layers/2)))
        elif weight_type == 'weak input' and block_type == 'input':
            weight = weight * 0.2
        elif weight_type == 'weak middle' and block_type == 'middle':
            weight = weight * 0.2
        elif weight_type == 'weak output' and block_type == 'output':
            weight = weight * 0.2
        elif weight_type == 'strong middle' and (block_type == 'input' or block_type == 'output'):
            weight = weight * 0.2
        elif isinstance(weight, dict):
            if t_idx not in weight:
                return 0, cond, uncond

            if weight_type == "style transfer precise":
                if layers == 11 and t_idx == 3:
                    uncond = cond
                    cond = cond * 0
                elif layers == 16 and (t_idx == 4 or t_idx == 5):
                    uncond = cond
                    cond = cond * 0
            elif weight_type == "composition precise":
                if layers == 11 and t_idx != 3:
                    uncond = cond
                    cond = cond * 0
                elif layers == 16 and (t_idx != 4 and t_idx != 5):
                    uncond = cond
                    cond = cond * 0

            weight = weight[t_idx]

            if cond_alt is not None and t_idx in cond_alt:
                cond = cond_alt[t_idx]
                del cond_alt
        return weight, cond, uncond

    def update_ipkv(self, weight, ip_k, ip_v, extra_options):
        # update ipadapter kv according to embeds scaling
        ipadapter_kwargs = extra_options.get("ipadapter_kwargs", None)
        embeds_scaling = ipadapter_kwargs[0]["embeds_scaling"]

        if embeds_scaling == 'K+mean(V) w/ C penalty':
            scaling = float(ip_k.shape[2]) / 1280.0
            weight = weight * scaling
            ip_k = ip_k * weight
            ip_v_mean = torch.mean(ip_v, dim=1, keepdim=True)
            ip_v = (ip_v - ip_v_mean) + ip_v_mean * weight
            del ip_v_mean
        elif embeds_scaling == 'K+V w/ C penalty':
            scaling = float(ip_k.shape[2]) / 1280.0
            weight = weight * scaling
            ip_k = ip_k * weight
            ip_v = ip_v * weight
        elif embeds_scaling == 'K+V':
            ip_k = ip_k * weight
            ip_v = ip_v * weight

        return embeds_scaling, ip_k, ip_v