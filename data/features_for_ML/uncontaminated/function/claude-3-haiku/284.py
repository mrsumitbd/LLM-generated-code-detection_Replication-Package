def get_str_len(text, fontSizeSet):
    total_length = 0
    for font_size in fontSizeSet:
        total_length += len(text) * font_size
    return total_length