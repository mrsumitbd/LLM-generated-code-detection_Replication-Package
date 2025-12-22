def apply_prompt_template(prompt_name: str, state: State, template: str = None) -> list:
    if template is None:
        template = get_prompt_template(prompt_name)
    
    prompt_parts = template.split("{}")
    
    prompts = []
    for i in range(len(prompt_parts) - 1):
        prompt = prompt_parts[i] + str(state.get_value(i))
        prompts.append(prompt)
    
    prompt = prompts[-1] + prompt_parts[-1]
    prompts.append(prompt)
    
    return prompts