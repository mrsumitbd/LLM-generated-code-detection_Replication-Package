def code_as_text(att: Attachment) -> Attachment:
    """
    Processes any file as plain text for code analysis, skipping binaries.
    If a directory is given, it delegates to the appropriate repository loader.
    """
    if att.is_directory():
        return _process_directory(att)
    elif att.is_binary():
        return att
    else:
        return _process_file(att)

def _process_directory(att: Attachment) -> Attachment:
    repo_loader = RepositoryLoader.for_path(att.path)
    if repo_loader:
        return repo_loader.load(att)
    else:
        return att

def _process_file(att: Attachment) -> Attachment:
    try:
        content = att.read_text()
        att.content = content
        return att
    except UnicodeDecodeError:
        return att