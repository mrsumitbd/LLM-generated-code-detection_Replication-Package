def apply_prompt_template(prompt_name: str, state: State, template: str = None) -> list:
    if template is None:
        template = state.get_default_template(prompt_name)
    return state.apply_template(template)