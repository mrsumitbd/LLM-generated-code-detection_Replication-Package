class SD3TextEncoder1StateDictConverter:

    def __init__(self):
        pass

    def from_diffusers(self, state_dict):
        converted_state_dict = {}
        
        for key, value in state_dict.items():
            # Remove 'text_model.' prefix if present
            if key.startswith('text_model.'):
                new_key = key.replace('text_model.', '', 1)
            else:
                new_key = key
            
            # Convert layer names
            new_key = new_key.replace('self_attn.', 'attention.')
            new_key = new_key.replace('q_proj', 'to_q')
            new_key = new_key.replace('k_proj', 'to_k')
            new_key = new_key.replace('v_proj', 'to_v')
            new_key = new_key.replace('out_proj', 'to_out.0')
            new_key = new_key.replace('fc1', 'net.0.proj')
            new_key = new_key.replace('fc2', 'net.2')
            new_key = new_key.replace('layer_norm1', 'norm1')
            new_key = new_key.replace('layer_norm2', 'norm2')
            new_key = new_key.replace('final_layer_norm', 'norm')
            
            converted_state_dict[new_key] = value
        
        return converted_state_dict

    def from_civitai(self, state_dict):
        converted_state_dict = {}
        
        for key, value in state_dict.items():
            new_key = key
            
            # Convert attention layer names
            new_key = new_key.replace('to_q', 'q_proj')
            new_key = new_key.replace('to_k', 'k_proj')
            new_key = new_key.replace('to_v', 'v_proj')
            new_key = new_key.replace('to_out.0', 'out_proj')
            
            # Convert MLP layer names
            new_key = new_key.replace('net.0.proj', 'fc1')
            new_key = new_key.replace('net.2', 'fc2')
            
            # Convert norm layer names
            new_key = new_key.replace('norm1', 'layer_norm1')
            new_key = new_key.replace('norm2', 'layer_norm2')
            new_key = new_key.replace('norm', 'final_layer_norm')
            
            # Convert attention to self_attn
            new_key = new_key.replace('attention.', 'self_attn.')
            
            # Add text_model prefix
            if not new_key.startswith('text_model.'):
                new_key = 'text_model.' + new_key
            
            converted_state_dict[new_key] = value
        
        return converted_state_dict