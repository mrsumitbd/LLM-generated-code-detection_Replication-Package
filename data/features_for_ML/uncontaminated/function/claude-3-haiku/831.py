def helper(sub):
    if not isinstance(sub, str):
        raise TypeError("Input must be a string")
    
    if not sub:
        return ""
    
    result = ""
    for char in sub:
        if char.isalnum():
            result += char.lower()
        else:
            result += "_"
    
    return result