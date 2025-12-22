from typing import Optional

class Dispacher:
    def __init__(self, args: "AutoCoderArgs", llm: Optional["AutoLLM"] = None):
        self.args = args
        self.llm = llm

    def dispach(self):
        if self.llm is None:
            raise ValueError("No LLM instance provided")
        prompt = getattr(self.args, "prompt", "")
        return self.llm.generate(prompt)