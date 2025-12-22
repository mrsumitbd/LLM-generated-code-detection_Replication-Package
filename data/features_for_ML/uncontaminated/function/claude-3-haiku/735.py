def __compress(result, target: str, power: int):
    if not target:
        return result
    
    char = target[0]
    count = 1
    
    for i in range(1, len(target)):
        if target[i] == char:
            count += 1
        else:
            if count > 1:
                result += str(count) + char
            else:
                result += char
            char = target[i]
            count = 1
    
    if count > 1:
        result += str(count) + char
    else:
        result += char
    
    return result