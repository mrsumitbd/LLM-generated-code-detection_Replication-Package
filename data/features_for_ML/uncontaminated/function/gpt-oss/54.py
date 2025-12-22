def generate_lossy_approval_comment(source_url, filenames, force_prompt_lossy_master=False):
    """
    Generate a comment for a pull request that contains lossy image files.

    Parameters
    ----------
    source_url : str
        The URL of the pull request or commit that triggered the check.
    filenames : Iterable[str]
        A list or iterable of file paths that were changed in the PR.
    force_prompt_lossy_master : bool, optional
        If True, always generate a comment regardless of the file types.

    Returns
    -------
    str
        A comment string that can be posted to the PR.  Returns an empty string
        if no lossy files are detected and the prompt is not forced.
    """
    # Define common lossy image extensions
    lossy_exts = {".jpg", ".jpeg", ".webp", ".avif", ".heif", ".heic"}

    # Normalize filenames to lower case for extension comparison
    lossy_files = [
        f for f in filenames
        if any(f.lower().endswith(ext) for ext in lossy_exts)
    ]

    # If no lossy files and not forced, return empty comment
    if not lossy_files and not force_prompt_lossy_master:
        return ""

    # Build the comment
    comment_lines = [
        "⚠️ **Lossy Image Detected**",
        "",
        "The following files in this PR are in lossy formats:",
    ]

    for f in lossy_files:
        comment_lines.append(f"- `{f}`")

    if not lossy_files:
        comment_lines.append("- (none detected, but forced prompt)")

    comment_lines.extend([
        "",
        f"Please review the impact of these changes. If lossless alternatives are available, consider using them.",
        "",
        f"[View PR]({source_url})",
    ])

    return "\n".join(comment_lines)