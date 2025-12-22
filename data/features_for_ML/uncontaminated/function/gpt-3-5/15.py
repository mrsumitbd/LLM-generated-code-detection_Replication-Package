def _create_github_url_error_attachment(att: Attachment) -> Attachment:
    return Attachment(
        title="Error",
        text="Invalid GitHub blob URL. Please provide a valid GitHub blob URL.",
        color="danger"
    )