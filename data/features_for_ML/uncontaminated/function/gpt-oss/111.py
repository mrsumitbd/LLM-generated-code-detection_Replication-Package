from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Iterable, Literal, Mapping

from enum import Enum, auto


class ProgrammingLanguage(Enum):
    PYTHON = auto()
    JAVASCRIPT = auto()
    TYPESCRIPT = auto()
    JAVA = auto()
    CSHARP = auto()
    CPP = auto()
    C = auto()
    RUBY = auto()
    GO = auto()
    PHP = auto()
    SWIFT = auto()
    KOTLIN = auto()
    UNKNOWN = auto()


# Mapping of file extensions to programming languages
EXTENSION_MAP: Mapping[str, ProgrammingLanguage] = {
    ".py": ProgrammingLanguage.PYTHON,
    ".js": ProgrammingLanguage.JAVASCRIPT,
    ".ts": ProgrammingLanguage.TYPESCRIPT,
    ".java": ProgrammingLanguage.JAVA,
    ".cs": ProgrammingLanguage.CSHARP,
    ".cpp": ProgrammingLanguage.CPP,
    ".c": ProgrammingLanguage.C,
    ".rb": ProgrammingLanguage.RUBY,
    ".go": ProgrammingLanguage.GO,
    ".php": ProgrammingLanguage.PHP,
    ".swift": ProgrammingLanguage.SWIFT,
    ".kt": ProgrammingLanguage.KOTLIN,
    ".kts": ProgrammingLanguage.KOTLIN,
}


def _count_languages(files: Iterable[Path]) -> Dict[ProgrammingLanguage, int]:
    counts: Dict[ProgrammingLanguage, int] = {}
    for f in files:
        ext = f.suffix.lower()
        lang = EXTENSION_MAP.get(ext)
        if lang:
            counts[lang] = counts.get(lang, 0) + 1
    return counts


def _most_common_language(counts: Dict[ProgrammingLanguage, int]) -> ProgrammingLanguage | None:
    if not counts:
        return None
    return max(counts.items(), key=lambda kv: kv[1])[0]


def _git_tracked_files(folder: Path) -> Iterable[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=str(folder),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    for line in result.stdout.splitlines():
        yield folder / line


def _folder_files(folder: Path) -> Iterable[Path]:
    for root, _, files in os.walk(folder):
        for name in files:
            yield Path(root) / name


def determine_project_language(
    folder_path: str,
    strategy: Literal["most_common", "git_most_common", "package_json"] = "git_most_common",
) -> ProgrammingLanguage:
    """
    Determines the primary programming language of a project.

    Args:
        folder_path (str): Path to the folder to analyze
        strategy (Literal["most_common", "git_most_common", "package_json"]): Strategy to use for determining language.
            "most_common" analyzes file extensions, "git_most_common" analyzes files in the git repo, "package_json" checks for package.json presence.

    Returns:
        ProgrammingLanguage: The determined programming language
    """
    folder = Path(folder_path).resolve()
    if not folder.is_dir():
        raise ValueError(f"Folder does not exist: {folder}")

    # Strategy: package_json
    if strategy == "package_json":
        pkg_path = folder / "package.json"
        if pkg_path.is_file():
            # Basic heuristic: if package.json exists, assume JavaScript/TypeScript
            # Try to read the "type" field for TS
            try:
                with pkg_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("type") == "module":
                    return ProgrammingLanguage.JAVASCRIPT
                # If there are TS dependencies, assume TS
                deps = data.get("dependencies", {})
                dev_deps = data.get("devDependencies", {})
                all_deps = {**deps, **dev_deps}
                if any(name.startswith("typescript") for name in all_deps):
                    return ProgrammingLanguage.TYPESCRIPT
            except Exception:
                pass
            return ProgrammingLanguage.JAVASCRIPT
        # Fall back to most_common if no package.json
        strategy = "most_common"

    # Strategy: git_most_common
    if strategy == "git_most_common":
        files = list(_git_tracked_files(folder))
        if files:
            counts = _count_languages(files)
            lang = _most_common_language(counts)
            if lang:
                return lang
        # Fall back to most_common if git fails or no language found
        strategy = "most_common"

    # Strategy: most_common
    if strategy == "most_common":
        files = list(_folder_files(folder))
        counts = _count_languages(files)
        lang = _most_common_language(counts)
        if lang:
            return lang

    # If nothing found, return UNKNOWN
    return ProgrammingLanguage.UNKNOWN