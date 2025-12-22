def system_prompt(natural=False, sab=False, **kwargs):
    import os
    import sys
    import platform

    prompt = ""

    if natural:
        prompt += "Natural language: "
    if sab:
        prompt += "SAB: "

    if 'text' in kwargs:
        prompt += kwargs['text']
    else:
        prompt += "System prompt"

    if 'color' in kwargs:
        color = kwargs['color']
        if sys.platform.startswith('win'):
            os.system(f"color {color}")
        else:
            prompt = f"\033[1;{color}m{prompt}\033[0m"

    if 'system' in kwargs:
        system = kwargs['system']
        prompt += f" ({system})"

    print(prompt)