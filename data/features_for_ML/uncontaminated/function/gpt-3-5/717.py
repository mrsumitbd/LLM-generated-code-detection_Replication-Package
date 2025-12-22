def _strip_properly_formatted_commas(expr: str):
    stack = []
    result = []
    for char in expr:
        if char == '(':
            stack.append('(')
        elif char == ')':
            if stack and stack[-1] == '(':
                stack.pop()
        elif char == ',' and not stack:
            continue
        result.append(char)
    return ''.join(result)