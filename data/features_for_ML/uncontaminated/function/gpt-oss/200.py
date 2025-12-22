import string

def INPUT_TYPES(s):
    """
    Analyze the input string `s` and return a dictionary with counts of
    different character categories:
        - 'digit': numeric characters 0-9
        - 'alpha': alphabetic characters a-z or A-Z
        - 'whitespace': space, tab, newline, carriage return, form feed, vertical tab
        - 'punctuation': any character in string.punctuation
        - 'other': any other character not covered above
    """
    counts = {
        'digit': 0,
        'alpha': 0,
        'whitespace': 0,
        'punctuation': 0,
        'other': 0
    }

    for ch in s:
        if ch.isdigit():
            counts['digit'] += 1
        elif ch.isalpha():
            counts['alpha'] += 1
        elif ch.isspace():
            counts['whitespace'] += 1
        elif ch in string.punctuation:
            counts['punctuation'] += 1
        else:
            counts['other'] += 1

    return counts