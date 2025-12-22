def get_nothink_str(llm: LLM):
    """
    Generates a "nothink" string based on the provided LLM object.

    Args:
        llm (LLM): An instance of the LLM class.

    Returns:
        str: A "nothink" string.
    """
    nothink_str = "nothink"
    for _ in range(llm.nothink_length):
        nothink_str += "nothink"
    return nothink_str