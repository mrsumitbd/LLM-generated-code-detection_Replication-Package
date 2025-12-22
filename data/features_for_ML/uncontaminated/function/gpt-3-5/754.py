def remove_illegal_characters(text):
    return ''.join(char for char in text if 32 <= ord(char) <= 126 or char in ['\t', '\n', '\r'])