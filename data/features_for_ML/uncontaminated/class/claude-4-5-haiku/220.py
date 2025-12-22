class Verifier:

    def __init__(self, llm_provider, model):
        self.llm_provider = llm_provider
        self.model = model

    def prompt(self, description: str, test_case: list[tuple[str, str]], gold_patch: str) -> str:
        test_case_str = "\n".join([f"Input: {inp}\nExpected Output: {out}" for inp, out in test_case])
        prompt = f"""You are a code verification expert. Given a description, test cases, and a patch, verify if the patch correctly solves the problem.

Description:
{description}

Test Cases:
{test_case_str}

Proposed Patch:
{gold_patch}

Please analyze if this patch correctly addresses the problem described and passes all test cases. Provide your verification result and reasoning."""
        return prompt

    def answer(self, description: str, test_case: list[tuple[str, str]], gold_patch: str) -> tuple[str, str]:
        prompt_text = self.prompt(description, test_case, gold_patch)
        response = self.llm_provider.generate(self.model, prompt_text)
        
        verification_result = "VERIFIED" if "correct" in response.lower() or "pass" in response.lower() else "FAILED"
        
        return (verification_result, response)

    def analyse_one_case(self, row):
        description = row.get("description", "")
        test_case = row.get("test_case", [])
        gold_patch = row.get("gold_patch", "")
        
        result, reasoning = self.answer(description, test_case, gold_patch)
        
        return {
            "result": result,
            "reasoning": reasoning,
            "description": description,
            "patch": gold_patch
        }

    def analyse_all(self, df: dict) -> list:
        results = []
        
        if isinstance(df, dict):
            rows = df.get("rows", []) if "rows" in df else list(df.values())
        else:
            rows = df
        
        for row in rows:
            analysis = self.analyse_one_case(row)
            results.append(analysis)
        
        return results