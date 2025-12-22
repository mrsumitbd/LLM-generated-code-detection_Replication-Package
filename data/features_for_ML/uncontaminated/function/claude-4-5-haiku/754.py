def remove_illegal_characters(text):
    # 去除 ASCII 控制字符（除了合法的制表符、换行符和回车符）
    return ''.join(char for char in text if ord(char) >= 32 or char in '\t\n\r')