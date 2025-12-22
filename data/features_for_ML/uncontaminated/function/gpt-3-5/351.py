def code_as_text(att: Attachment) -> Attachment:
    if att.is_binary():
        return att
    if att.is_directory():
        return load_repository(att)
    return att