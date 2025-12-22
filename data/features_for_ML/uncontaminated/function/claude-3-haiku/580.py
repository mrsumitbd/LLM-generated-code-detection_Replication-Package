def replace_context(match):
    text = match.group()
    context = match.group('context')
    replacement = match.group('replacement')
    return text.replace(context, replacement)