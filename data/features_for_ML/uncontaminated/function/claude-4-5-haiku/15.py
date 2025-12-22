def _create_github_url_error_attachment(att: Attachment) -> Attachment:
    """Create a helpful error attachment for GitHub blob URLs."""
    error_message = (
        "GitHub blob URLs are not supported. "
        "Please use the raw content URL instead.\n\n"
        "To get the raw URL:\n"
        "1. Navigate to the file on GitHub\n"
        "2. Click the 'Raw' button\n"
        "3. Copy the URL from the address bar\n\n"
        "Or replace '/blob/' with '/raw/' in the URL."
    )
    
    return Attachment(
        name=att.name if hasattr(att, 'name') else "error",
        data=error_message.encode('utf-8'),
        mime_type="text/plain"
    )