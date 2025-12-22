def get_nothink_str(llm: LLM):
    """
    Ask the LLM to output the string 'nothink' and return the result.

    Parameters
    ----------
    llm : LLM
        An instance of an LLM that supports either `invoke` or `generate`.

    Returns
    -------
    str
        The string produced by the LLM, stripped of surrounding whitespace.
    """
    # Prompt that explicitly requests only the word "nothink"
    prompt = "Please output the string 'nothink' only, with no additional text."

    # Try the common LangChain `invoke` method first
    try:
        result = llm.invoke(prompt)
    except AttributeError:
        # Fallback to the older `generate` method if `invoke` is not available
        result = llm.generate(prompt)

    # Convert to string (in case the LLM returns a different type) and strip whitespace
    return str(result).strip()