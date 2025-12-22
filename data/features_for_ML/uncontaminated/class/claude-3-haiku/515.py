class PromptFormatter:
    def __init__(self, t2i, opt):
        self.t2i = t2i
        self.opt = opt
        self.prompt = None

    def normalize_prompt(self):
        if self.prompt is None:
            return ""

        tokens = self.prompt.strip().split()
        normalized_tokens = []
        for token in tokens:
            if token.lower() in self.t2i:
                normalized_tokens.append(self.t2i[token.lower()])
            else:
                normalized_tokens.append(self.t2i[self.opt])

        return " ".join(map(str, normalized_tokens))