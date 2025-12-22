def code_as_text(att: Attachment) -> Attachment:
    """
    Processes any file as plain text for code analysis, skipping binaries.
    If a directory is given, it delegates to the appropriate repository loader.
    """
    import os
    import mimetypes
    from pathlib import Path
    
    if att.path is None:
        return att
    
    path = Path(att.path)
    
    # Handle directories
    if path.is_dir():
        # Check for repository indicators
        if (path / '.git').exists():
            from .loaders import git_loader
            return git_loader(att)
        elif (path / '.hg').exists():
            from .loaders import hg_loader
            return hg_loader(att)
        elif (path / '.svn').exists():
            from .loaders import svn_loader
            return svn_loader(att)
        else:
            # Generic directory loader
            from .loaders import directory_loader
            return directory_loader(att)
    
    # Handle files
    if path.is_file():
        # Check if file is binary
        mime_type, _ = mimetypes.guess_type(str(path))
        
        # List of binary MIME types to skip
        binary_types = {
            'application/octet-stream',
            'application/x-executable',
            'application/x-sharedlib',
            'application/x-object',
            'image/',
            'audio/',
            'video/',
            'application/pdf',
            'application/zip',
            'application/gzip',
            'application/x-tar',
        }
        
        # Check MIME type
        if mime_type:
            if any(mime_type.startswith(bt.rstrip('/')) for bt in binary_types):
                return att
        
        # Try to read as text
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            att.content = content
            return att
        except (UnicodeDecodeError, IOError):
            # File is binary or unreadable, skip it
            return att
    
    return att