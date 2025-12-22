class Verifier:

    def __init__(self, llm_provider, model):
        self.llm_provider = llm_provider
        self.model = model

    def prompt(self, description: str, test_case: list[tuple[str, str]], gold_patch: str) -> str:
        pass

    def answer(self, description: str, test_case: list[tuple[str, str]], gold_patch: str) -> tuple[str, str]:
        pass

    def analyse_one_case(self, row):
        pass

    def analyse_all(self, df: dict) -> list:
        pass