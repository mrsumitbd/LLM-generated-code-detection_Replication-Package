class SDUNetStateDictConverter:

    def __init__(self):
        pass

    def from_diffusers(self, state_dict):
        """Convert state dict from diffusers format to internal format"""
        converted = {}
        for key, value in state_dict.items():
            # Remove 'unet.' prefix if present
            new_key = key.replace('unet.', '') if key.startswith('unet.') else key
            converted[new_key] = value
        return converted

    def from_civitai(self, state_dict):
        """Convert state dict from CivitAI format to internal format"""
        converted = {}
        for key, value in state_dict.items():
            # CivitAI models may have different naming conventions
            # Map common CivitAI keys to standard format
            new_key = key
            
            # Handle various CivitAI naming patterns
            if key.startswith('model.diffusion_model.'):
                new_key = key.replace('model.diffusion_model.', '')
            elif key.startswith('diffusion_model.'):
                new_key = key.replace('diffusion_model.', '')
            elif key.startswith('unet.'):
                new_key = key.replace('unet.', '')
            
            converted[new_key] = value
        
        return converted