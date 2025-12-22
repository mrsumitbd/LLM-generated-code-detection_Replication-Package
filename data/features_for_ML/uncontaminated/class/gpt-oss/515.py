import re

class PromptFormatter:
    def __init__(self, t2i, opt):
        """
        Initialize the PromptFormatter.

        Parameters
        ----------
        t2i : str
            The raw prompt string to be normalized.
        opt : dict
            Options dictionary. Supported keys:
                - 'max_length' (int): maximum length of the normalized prompt.
        """
        self.t2i = t2i
        self.opt = opt or {}

    def normalize_prompt(self):
        """
        Normalize the prompt string.

        Returns
        -------
        str
            The normalized prompt.
        """
        if not isinstance(self.t2i, str):
            raise TypeError("t2i must be a string prompt")

        # Strip leading/trailing whitespace and convert to lowercase
        prompt = self.t2i.strip().lower()

        # Remove punctuation (keep alphanumeric and spaces)
        prompt = re.sub(r'[^\w\s]', '', prompt)

        # Collapse multiple whitespace into a single space
        prompt = re.sub(r'\s+', ' ', prompt)

        # Truncate to max_length if specified
        max_len = self.opt.get('max_length')
        if isinstance(max_len, int) and max_len > 0:
            prompt = prompt[:max_len]

        return prompt