from typing import Any, Dict

# Define a minimal Attachment type for type checking.
Attachment = Dict[str, Any]


def _create_github_url_error_attachment(att: Attachment) -> Attachment:
    """
    Create a helpful error attachment for GitHub blob URLs.

    Parameters
    ----------
    att : Attachment
        The original attachment that triggered the error. It is ignored
        in the construction of the error attachment but is kept in the
        signature for consistency with the surrounding code.

    Returns
    -------
    Attachment
        A new attachment dictionary containing a user‑friendly error
        message and styling information.
    """
    # Base error attachment
    error_attachment: Attachment = {
        "fallback": "Invalid GitHub URL",
        "color": "#ff0000",  # Red color to indicate error
        "title": "Invalid GitHub URL",
        "text": (
            "The URL you provided does not appear to be a valid GitHub blob URL.\n\n"
            "A valid GitHub blob URL should look like this:\n"
            "`https://github.com/<user>/<repo>/blob/<branch>/<path>`\n\n"
            "If you intended to link to a raw file, use the raw URL instead, e.g.:\n"
            "`https://raw.githubusercontent.com/<user>/<repo>/<branch>/<path>`\n\n"
            "Please double‑check the URL and try again."
        ),
        "mrkdwn_in": ["text"],
    }

    return error_attachment