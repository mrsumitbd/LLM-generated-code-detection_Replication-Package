def _extract_param_type(docstring, param_name):
    if not docstring:
        return None
    param_type = None
    lines = docstring.split('\n')
    for line in lines:
        if f'{param_name} :' in line:
            param_type = line.split(':')[1].strip()
            break
    return param_type