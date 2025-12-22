def system_prompt(natural=False, sab=False, **kwargs):
    """
    Generate a system prompt string for a language model.

    Parameters
    ----------
    natural : bool, optional
        If True, use a natural‑language style prompt.
    sab : bool, optional
        If True, use a system‑assistant‑bot style prompt.
    **kwargs : dict, optional
        Additional keyword arguments to customize the prompt.
        Supported keys:
            - template : str
                Override the entire prompt template.
            - instructions : str
                Append custom instructions to the prompt.
            - role : str
                Prefix the prompt with a role name.

    Returns
    -------
    str
        The constructed system prompt.
    """
    # Default prompt templates
    templates = {
        "default": (
            "You are a helpful assistant. "
            "Respond to the user in a concise and friendly manner."
        ),
        "natural": (
            "You are a friendly assistant. "
            "Speak naturally and politely."
        ),
        "sab": (
            "You are a system assistant bot. "
            "Provide accurate and concise answers."
        ),
    }

    # Choose template based on flags
    if sab:
        template = templates["sab"]
    elif natural:
        template = templates["natural"]
    else:
        template = templates["default"]

    # Allow full template override
    if "template" in kwargs:
        template = kwargs["template"]

    # Append custom instructions if provided
    instructions = kwargs.get("instructions")
    if instructions:
        template = f"{template} {instructions}"

    # Prefix with role name if provided
    role = kwargs.get("role")
    if role:
        template = f"{role}: {template}"

    return template