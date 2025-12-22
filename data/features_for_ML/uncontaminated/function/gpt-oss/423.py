def run_text_guardrail(prompt: str, guardrail_runner: "GuardrailRunner") -> bool:
    """
    Run the text guardrail on the prompt, checking for content safety.

    Args:
        prompt: The text prompt.
        guardrail_runner: The text guardrail runner.

    Returns:
        bool: Whether the prompt is safe.
    """
    try:
        # Execute the guardrail runner. The exact API may vary, so we handle
        # several common patterns.
        result = guardrail_runner.run(prompt)

        # If the result is a boolean, return it directly.
        if isinstance(result, bool):
            return result

        # If the result is a mapping with a 'safe' key, use that.
        if isinstance(result, dict) and "safe" in result:
            return bool(result["safe"])

        # If the result has an attribute named 'safe', use it.
        if hasattr(result, "safe"):
            return bool(getattr(result, "safe"))

        # If the result has an attribute named 'is_safe', use it.
        if hasattr(result, "is_safe"):
            return bool(getattr(result, "is_safe"))

        # If the result has a method that returns a boolean, try it.
        if hasattr(result, "is_safe") and callable(getattr(result, "is_safe")):
            return bool(result.is_safe())

        # If the result has a method that returns a dict with 'safe', try it.
        if hasattr(result, "to_dict") and callable(getattr(result, "to_dict")):
            dict_result = result.to_dict()
            if isinstance(dict_result, dict) and "safe" in dict_result:
                return bool(dict_result["safe"])

    except Exception:
        # Any exception during guardrail execution is treated as unsafe.
        pass

    # Default to unsafe if we cannot determine safety.
    return False