def _create_github_url_error_attachment(att: Attachment) -> Attachment:
    """Create a helpful error attachment for GitHub blob URLs."""
    error_message = (
        "The provided URL does not appear to be a valid GitHub blob URL. "
        "Please ensure the URL is in the format: "
        "https://github.com/owner/repo/blob/branch/path/to/file.ext"
    )
    return Attachment(
        title="Invalid GitHub URL",
        text=error_message,
        color="danger",
    )