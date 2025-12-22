def replace_context(match):
    return match.group(0).replace('{{', '').replace('}}', '')