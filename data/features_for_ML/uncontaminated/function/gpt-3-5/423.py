def run_text_guardrail(prompt: str, guardrail_runner: GuardrailRunner) -> bool:
    return guardrail_runner.run_guardrail(prompt)