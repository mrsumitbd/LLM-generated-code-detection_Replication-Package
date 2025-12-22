import openai
import pandas as pd

class Verifier:

    def __init__(self, llm_provider, model):
        self.llm_provider = llm_provider
        self.model = model
        openai.api_key = self.llm_provider

    def prompt(self, description: str, test_case: list[tuple[str, str]], gold_patch: str) -> str:
        prompt = f"Given the following description:\n{description}\n\nAnd the following test cases:\n"
        for input_text, expected_output in test_case:
            prompt += f"Input: {input_text}\nExpected Output: {expected_output}\n"
        prompt += f"\nGenerate a Python code patch that passes all the test cases and matches the provided gold patch: {gold_patch}"
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()

    def answer(self, description: str, test_case: list[tuple[str, str]], gold_patch: str) -> tuple[str, str]:
        generated_patch = self.prompt(description, test_case, gold_patch)
        result = self.analyse_one_case((description, test_case, gold_patch, generated_patch))
        return generated_patch, result

    def analyse_one_case(self, row):
        description, test_case, gold_patch, generated_patch = row
        for input_text, expected_output in test_case:
            try:
                actual_output = eval(generated_patch.strip())
                if actual_output != expected_output:
                    return f"Test case failed: Input={input_text}, Expected={expected_output}, Actual={actual_output}"
            except Exception as e:
                return f"Error in generated patch: {e}"
        return "All test cases passed"

    def analyse_all(self, df: dict) -> list:
        results = []
        for row in df.values():
            results.append(self.analyse_one_case(row))
        return results