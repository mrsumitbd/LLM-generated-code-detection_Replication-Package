def validate_expression(expression: str, allowed_keys: list[str]) -> None:
    stack = []
    opening_brackets = set(['(', '[', '{'])
    closing_brackets = set([')', ']', '}'])
    bracket_pairs = {')': '(', ']': '[', '}': '{'}
    
    for char in expression:
        if char in opening_brackets:
            stack.append(char)
        elif char in closing_brackets:
            if not stack or stack[-1] != bracket_pairs[char]:
                print("Invalid expression")
                return
            stack.pop()
        elif char in allowed_keys:
            continue
        else:
            print("Invalid expression")
            return
    
    if stack:
        print("Invalid expression")
    else:
        print("Valid expression")