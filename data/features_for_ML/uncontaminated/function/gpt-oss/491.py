def preprocess(sample, is_cot=False):
    """
    Preprocess a sample dictionary into a prompt string.

    Parameters
    ----------
    sample : dict
        A dictionary that should contain at least a 'question' key and either
        an 'answer' key or a 'cot' (chain‑of‑thought) key.
    is_cot : bool, optional
        If True, the function will use the 'cot' field as the answer; otherwise
        it will use the 'answer' field.

    Returns
    -------
    str
        A formatted prompt string of the form:
            "Question: <question>\nAnswer: <answer>"
    """
    # Extract the question, ensuring it is a string and stripping whitespace
    question = str(sample.get("question", "")).strip()

    # Choose the answer field based on the is_cot flag
    if is_cot:
        answer = str(sample.get("cot", "")).strip()
    else:
        answer = str(sample.get("answer", "")).strip()

    # Build the prompt
    prompt = f"Question: {question}\nAnswer: {answer}"
    return prompt