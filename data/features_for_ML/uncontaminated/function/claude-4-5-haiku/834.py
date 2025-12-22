def apply_prompt_template(prompt_name: str, state: State, template: str = None) -> list:
    """
    Apply a prompt template to the current state and return a list of formatted prompts.
    
    Args:
        prompt_name: Name identifier for the prompt
        state: State object containing context variables
        template: Optional template string to use instead of default
    
    Returns:
        List of formatted prompt strings
    """
    if template is None:
        template = get_default_template(prompt_name)
    
    if not template:
        return []
    
    state_dict = state.to_dict() if hasattr(state, 'to_dict') else vars(state)
    
    try:
        formatted_prompt = template.format(**state_dict)
        return [formatted_prompt]
    except KeyError as e:
        missing_key = str(e).strip("'")
        if hasattr(state, 'get_default'):
            state_dict[missing_key] = state.get_default(missing_key)
            formatted_prompt = template.format(**state_dict)
            return [formatted_prompt]
        return []
    except Exception:
        return []


def get_default_template(prompt_name: str) -> str:
    """Helper function to retrieve default templates by name."""
    templates = {
        "default": "Prompt: {input}",
        "chat": "User: {message}\nAssistant:",
        "completion": "{context}\n{prompt}",
    }
    return templates.get(prompt_name, "")