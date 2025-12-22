def extract_from_tag_block(txt: str, tag: str) -> str:
    start_tag = f"<{tag}>"
    end_tag = f"</{tag}>"
    start_index = txt.find(start_tag)
    if start_index == -1:
        return ""
    start_index += len(start_tag)
    end_index = txt.find(end_tag, start_index)
    if end_index == -1:
        return ""
    return txt[start_index:end_index]