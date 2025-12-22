def get_str_len(text, fontSizeSet):
    total_len = 0
    for char in text:
        font_size = fontSizeSet.get(char, 1)
        total_len += font_size
    return total_len