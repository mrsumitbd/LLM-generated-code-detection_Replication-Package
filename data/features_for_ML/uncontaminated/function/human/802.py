import re

def extract_from_tag_block(txt: str, tag: str) -> str:
    pattern = rf"<{re.escape(tag)}>\n(.*?)\n</{re.escape(tag)}>"
    match = re.search(pattern, txt, flags=re.DOTALL)
    return match.group(1) if match else ""