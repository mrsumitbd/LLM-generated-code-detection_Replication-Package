def generate_lossy_approval_comment(source_url, filenames, force_prompt_lossy_master=False):
    import os
    import re

    comment = ""
    for filename in filenames:
        if filename.endswith(".jpg") or filename.endswith(".png"):
            comment += f"Approved {filename} (Lossy)\n"
        else:
            comment += f"Approved {filename}\n"

    if force_prompt_lossy_master or any(filename.endswith(".jpg") or filename.endswith(".png") for filename in filenames):
        comment += "\nWarning: This PR contains lossy image files (JPG/PNG). Please ensure that the image quality is acceptable before merging."

    return comment.strip()