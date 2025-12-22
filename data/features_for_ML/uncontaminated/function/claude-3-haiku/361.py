def process(s):
    words = s.split()
    result = []
    for word in words:
        if len(word) > 3:
            result.append(word.upper())
        else:
            result.append(word.lower())
    return ' '.join(result)