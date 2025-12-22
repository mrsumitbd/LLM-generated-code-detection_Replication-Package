from typing import Literal
from collections import Counter
import os
import subprocess
import json

ProgrammingLanguage = str

def determine_project_language(folder_path: str, strategy: Literal["most_common", "git_most_common", "package_json"] = "git_most_common") -> ProgrammingLanguage:
    """Determines the primary programming language of a project.

    Args:
        folder_path (str): Path to the folder to analyze
        strategy (Literal["most_common", "git_most_common", "package_json"]): Strategy to use for determining language.
            "most_common" analyzes file extensions, "git_most_common" analyzes files in the git repo, "package_json" checks for package.json presence.

    Returns:
        ProgrammingLanguage: The determined programming language
    """
    if strategy == "most_common":
        return _determine_language_by_file_extensions(folder_path)
    elif strategy == "git_most_common":
        return _determine_language_by_git_repo(folder_path)
    elif strategy == "package_json":
        return _determine_language_by_package_json(folder_path)
    else:
        raise ValueError(f"Invalid strategy: {strategy}")

def _determine_language_by_file_extensions(folder_path: str) -> ProgrammingLanguage:
    file_extensions = [os.path.splitext(f)[1][1:] for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    extension_counts = Counter(file_extensions)
    return max(extension_counts, key=extension_counts.get)

def _determine_language_by_git_repo(folder_path: str) -> ProgrammingLanguage:
    try:
        output = subprocess.check_output(["git", "ls-files"], cwd=folder_path)
        file_extensions = [os.path.splitext(f)[1][1:] for f in output.decode().splitlines()]
        extension_counts = Counter(file_extensions)
        return max(extension_counts, key=extension_counts.get)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Unknown"

def _determine_language_by_package_json(folder_path: str) -> ProgrammingLanguage:
    package_json_path = os.path.join(folder_path, "package.json")
    if os.path.isfile(package_json_path):
        with open(package_json_path, "r") as f:
            package_json = json.load(f)
        if "language" in package_json:
            return package_json["language"]
    return "Unknown"