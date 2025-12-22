import re

def remove_illegal_characters(text):
    # 去除 ASCII 控制字符（除了合法的制表符、换行符和回车符）
    illegal_chars = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")
    return illegal_chars.sub("", text)