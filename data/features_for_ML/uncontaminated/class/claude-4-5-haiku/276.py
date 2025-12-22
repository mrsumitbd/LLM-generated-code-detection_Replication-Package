import anthropic


class CogVAEDecoderStateDictConverter:

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"

    def from_diffusers(self, state_dict):
        """Convert state dict from diffusers format to standard format."""
        prompt = f"""You are an expert in converting PyTorch model state dictionaries between different formats.

Given a state dictionary from the diffusers library for a CogVAE decoder, convert it to the standard format.

Input state dict keys (sample):
{list(state_dict.keys())[:10]}

Please provide the conversion mapping as a Python dictionary where keys are the original diffusers format keys and values are the target format keys. Only return the Python dictionary, no other text."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        converted_dict = {}
        for key, value in state_dict.items():
            new_key = key
            if "decoder" in key:
                new_key = key.replace("decoder.", "")
            converted_dict[new_key] = value
        
        return converted_dict

    def from_civitai(self, state_dict):
        """Convert state dict from CivitAI format to standard format."""
        prompt = f"""You are an expert in converting PyTorch model state dictionaries between different formats.

Given a state dictionary from CivitAI for a CogVAE decoder, convert it to the standard format.

Input state dict keys (sample):
{list(state_dict.keys())[:10]}

Please provide the conversion mapping as a Python dictionary where keys are the original CivitAI format keys and values are the target format keys. Only return the Python dictionary, no other text."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        converted_dict = {}
        for key, value in state_dict.items():
            new_key = key
            if "vae_decoder" in key:
                new_key = key.replace("vae_decoder.", "")
            elif "first_stage_model.decoder" in key:
                new_key = key.replace("first_stage_model.decoder.", "")
            converted_dict[new_key] = value
        
        return converted_dict