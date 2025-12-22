def _extract_param_type(docstring, param_name):
    """
    Extracts the parameter type from the function's docstring.
    """
    try:
        param_section = next(section for section in docstring.split('\n\n') if f':{param_name}:' in section)
        param_type = next(line.strip() for line in param_section.split('\n') if line.strip().startswith(':type'))
        return param_type.split(':')[2].strip()
    except (StopIteration, IndexError):
        return None