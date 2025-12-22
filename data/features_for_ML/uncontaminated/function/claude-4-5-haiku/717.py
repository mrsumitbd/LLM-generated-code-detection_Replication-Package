def _strip_properly_formatted_commas(expr: str):
    # We want to be careful because we don't want to strip tuple commas
    result = []
    paren_depth = 0
    bracket_depth = 0
    brace_depth = 0
    
    i = 0
    while i < len(expr):
        char = expr[i]
        
        if char == '(':
            paren_depth += 1
            result.append(char)
        elif char == ')':
            paren_depth -= 1
            result.append(char)
        elif char == '[':
            bracket_depth += 1
            result.append(char)
        elif char == ']':
            bracket_depth -= 1
            result.append(char)
        elif char == '{':
            brace_depth += 1
            result.append(char)
        elif char == '}':
            brace_depth -= 1
            result.append(char)
        elif char == ',' and paren_depth == 0 and bracket_depth == 0 and brace_depth == 0:
            # Skip commas at the top level (not inside any brackets)
            pass
        else:
            result.append(char)
        
        i += 1
    
    return ''.join(result)