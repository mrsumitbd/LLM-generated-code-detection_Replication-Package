from cosmos_predict2.auxiliary.guardrail.common.core import GuardrailRunner
from imaginaire.utils import log

def run_text_guardrail(prompt: str, guardrail_runner: GuardrailRunner) -> bool:
    """Run the text guardrail on the prompt, checking for content safety.

    Args:
        prompt: The text prompt.
        guardrail_runner: The text guardrail runner.

    Returns:
        bool: Whether the prompt is safe.
    """
    is_safe, message = guardrail_runner.run_safety_check(prompt)
    if not is_safe:
        log.critical(f"GUARDRAIL BLOCKED: {message}")
    return is_safe