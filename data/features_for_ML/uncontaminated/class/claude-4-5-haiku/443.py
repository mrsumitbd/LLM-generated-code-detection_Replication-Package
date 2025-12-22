class Dispacher:

    def __init__(self, args: AutoCoderArgs, llm: Optional[AutoLLM] = None):
        self.args = args
        self.llm = llm
        self._validate_args()

    def _validate_args(self):
        if self.args is None:
            raise ValueError("AutoCoderArgs cannot be None")

    def dispach(self):
        if self.llm is None:
            raise ValueError("LLM is not initialized")
        
        if not hasattr(self.args, 'action'):
            raise ValueError("AutoCoderArgs must have an 'action' attribute")
        
        action = self.args.action
        
        if action == "generate":
            return self._handle_generate()
        elif action == "refactor":
            return self._handle_refactor()
        elif action == "test":
            return self._handle_test()
        elif action == "analyze":
            return self._handle_analyze()
        else:
            raise ValueError(f"Unknown action: {action}")

    def _handle_generate(self):
        return self.llm.generate(self.args)

    def _handle_refactor(self):
        return self.llm.refactor(self.args)

    def _handle_test(self):
        return self.llm.test(self.args)

    def _handle_analyze(self):
        return self.llm.analyze(self.args)