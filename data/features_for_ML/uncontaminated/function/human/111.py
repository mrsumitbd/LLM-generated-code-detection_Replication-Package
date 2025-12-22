from typing import Literal
from codegen.shared.enums.programming_language import ProgrammingLanguage

def determine_project_language(folder_path: str, strategy: Literal["most_common", "git_most_common", "package_json"] = "git_most_common") -> ProgrammingLanguage:
    """Determines the primary programming language of a project.

    Args:
        folder_path (str): Path to the folder to analyze
        strategy (Literal["most_common", "git_most_common", "package_json"]): Strategy to use for determining language.
            "most_common" analyzes file extensions, "git_most_common" analyzes files in the git repo, "package_json" checks for package.json presence.

    Returns:
        ProgrammingLanguage: The determined programming language
    """
    # TODO: Create a new strategy that follows gitignore
    if strategy == "most_common":
        return _determine_language_by_file_count(folder_path)
    elif strategy == "git_most_common":
        return _determine_language_by_git_file_count(folder_path)
    elif strategy == "package_json":
        return _determine_language_by_package_json(folder_path)
    else:
        msg = f"Invalid strategy: {strategy}"
        raise ValueError(msg)