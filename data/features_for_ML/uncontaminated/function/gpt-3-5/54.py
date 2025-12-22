def generate_lossy_approval_comment(source_url, filenames, force_prompt_lossy_master=False):
    comment = f"Please review the following files for approval: {', '.join(filenames)} from {source_url}"
    if force_prompt_lossy_master:
        comment += " (Force prompt for lossy master)"
    return comment