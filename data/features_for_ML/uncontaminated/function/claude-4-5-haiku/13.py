def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
    """
    Apply consistent spacing around assignment operators.

    Args:
        line: The line to format
        use_spaces: Whether to use spaces around operators

    Returns:
        The formatted line
    """
    import re
    
    # Don't modify strings or comments
    if not line.strip() or line.strip().startswith('#'):
        return line
    
    # Preserve leading whitespace
    leading_spaces = len(line) - len(line.lstrip())
    content = line[leading_spaces:]
    
    # Skip if line contains string literals (simple heuristic)
    if '"""' in content or "'''" in content:
        return line
    
    # Handle single and double quoted strings - don't modify inside them
    in_string = False
    string_char = None
    result = []
    i = 0
    
    while i < len(content):
        char = content[i]
        
        # Track string state
        if char in ('"', "'") and (i == 0 or content[i-1] != '\\'):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None
        
        # Process assignment operators only outside strings
        if not in_string and char == '=' and (i == 0 or content[i-1] not in '!<>=-+*/%&|^'):
            # Check if it's not part of ==, !=, <=, >=, etc.
            if i + 1 < len(content) and content[i+1] == '=':
                result.append(char)
                i += 1
                continue
            
            # Remove spaces before =
            while result and result[-1] == ' ':
                result.pop()
            
            if use_spaces:
                result.append(' = ')
            else:
                result.append('=')
            
            # Skip spaces after =
            i += 1
            while i < len(content) and content[i] == ' ':
                i += 1
            continue
        
        result.append(char)
        i += 1
    
    return ' ' * leading_spaces + ''.join(result)