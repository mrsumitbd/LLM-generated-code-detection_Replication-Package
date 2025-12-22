def run_text_guardrail(prompt: str, guardrail_runner: GuardrailRunner) -> bool:
    """Run the text guardrail on the prompt, checking for content safety.

    Args:
        prompt: The text prompt.
        guardrail_runner: The text guardrail runner.

    Returns:
        bool: Whether the prompt is safe.
    """
    try:
        result = guardrail_runner.run_guardrail(prompt)
        return result.is_safe
    except Exception:
        return False