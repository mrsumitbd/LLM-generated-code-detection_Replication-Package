def process(s):
    result = ""
    for char in s:
        if char.isalpha():
            result += char.upper()
        else:
            result += char
    return result