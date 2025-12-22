def get_str_len(text, fontSizeSet):
    width = 0
    for char in text:
        if ord(char) > 0x2E80:  # chinese char
            width += 2
        elif char in "[](){}「」【】《》":
            width += 2
        else:
            width += 1
    return width * (fontSizeSet / 2)