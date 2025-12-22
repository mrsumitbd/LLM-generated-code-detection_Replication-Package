def remove_illegal_characters(text):
    return ''.join(char for char in text if char in '\t\n\r' or 32 <= ord(char) <= 126)