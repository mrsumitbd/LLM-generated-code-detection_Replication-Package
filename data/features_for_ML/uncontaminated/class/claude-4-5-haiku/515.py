class PromptFormatter:

    def __init__(self, t2i, opt):
        self.t2i = t2i
        self.opt = opt

    def normalize_prompt(self):
        prompt = self.opt.get('prompt', '')
        
        # Remove extra whitespace
        prompt = ' '.join(prompt.split())
        
        # Convert to lowercase if specified
        if self.opt.get('lowercase', False):
            prompt = prompt.lower()
        
        # Remove special characters if specified
        if self.opt.get('remove_special_chars', False):
            import string
            prompt = ''.join(c for c in prompt if c.isalnum() or c.isspace())
        
        # Truncate to max length if specified
        max_length = self.opt.get('max_length', None)
        if max_length and len(prompt) > max_length:
            prompt = prompt[:max_length]
        
        # Strip leading/trailing whitespace
        prompt = prompt.strip()
        
        return prompt