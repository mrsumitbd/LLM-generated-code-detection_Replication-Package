import os
from attachments.loaders.repositories.utils import is_likely_binary
from attachments.core import Attachment, presenter
from attachments import load, present
from attachments.loaders.repositories import directory_to_structure, git_repo_to_structure
from attachments.matchers import git_repo_match

def code_as_text(att: Attachment) -> Attachment:
    """
    Processes any file as plain text for code analysis, skipping binaries.
    If a directory is given, it delegates to the appropriate repository loader.
    """
    from attachments import load, present

    # If it's a file, process it directly
    if os.path.isfile(att.path):
        if is_likely_binary(att.path):
            att.text = ""
            att.metadata["skipped_binary"] = True
            return att
        return att | load.text_to_string | present.code

    # If it's a directory, delegate to the correct loader
    if os.path.isdir(att.path):
        from attachments.loaders.repositories import directory_to_structure, git_repo_to_structure
        from attachments.matchers import git_repo_match

        if git_repo_match(att):
            return git_repo_to_structure(att)
        else:
            return directory_to_structure(att)

    # Fallback for things that aren't files or directories (e.g. URLs to be morphed)
    # The processor will run again after morphing.
    return att