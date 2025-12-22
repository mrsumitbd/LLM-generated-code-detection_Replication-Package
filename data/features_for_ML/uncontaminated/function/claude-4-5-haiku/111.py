def determine_project_language(folder_path: str, strategy: Literal["most_common", "git_most_common", "package_json"] = "git_most_common") -> ProgrammingLanguage:
    """Determines the primary programming language of a project.

    Args:
        folder_path (str): Path to the folder to analyze
        strategy (Literal["most_common", "git_most_common", "package_json"]): Strategy to use for determining language.
            "most_common" analyzes file extensions, "git_most_common" analyzes files in the git repo, "package_json" checks for package.json presence.

    Returns:
        ProgrammingLanguage: The determined programming language
    """
    import os
    import subprocess
    from collections import Counter
    from pathlib import Path
    
    # Map file extensions to programming languages
    extension_map = {
        '.py': ProgrammingLanguage.PYTHON,
        '.js': ProgrammingLanguage.JAVASCRIPT,
        '.ts': ProgrammingLanguage.TYPESCRIPT,
        '.jsx': ProgrammingLanguage.JAVASCRIPT,
        '.tsx': ProgrammingLanguage.TYPESCRIPT,
        '.java': ProgrammingLanguage.JAVA,
        '.cpp': ProgrammingLanguage.CPP,
        '.c': ProgrammingLanguage.C,
        '.cs': ProgrammingLanguage.CSHARP,
        '.go': ProgrammingLanguage.GO,
        '.rs': ProgrammingLanguage.RUST,
        '.rb': ProgrammingLanguage.RUBY,
        '.php': ProgrammingLanguage.PHP,
        '.swift': ProgrammingLanguage.SWIFT,
        '.kt': ProgrammingLanguage.KOTLIN,
        '.scala': ProgrammingLanguage.SCALA,
        '.r': ProgrammingLanguage.R,
        '.m': ProgrammingLanguage.OBJECTIVE_C,
        '.mm': ProgrammingLanguage.OBJECTIVE_C,
        '.pl': ProgrammingLanguage.PERL,
        '.lua': ProgrammingLanguage.LUA,
        '.sh': ProgrammingLanguage.SHELL,
        '.bash': ProgrammingLanguage.SHELL,
    }
    
    def get_files_by_extension(path: str) -> Counter:
        """Count files by extension in the directory."""
        extension_count = Counter()
        try:
            for root, dirs, files in os.walk(path):
                # Skip hidden directories and common non-source directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
                for file in files:
                    ext = Path(file).suffix.lower()
                    if ext in extension_map:
                        extension_count[ext] += 1
        except Exception:
            pass
        return extension_count
    
    def get_git_files() -> Counter:
        """Get files tracked by git and count by extension."""
        extension_count = Counter()
        try:
            result = subprocess.run(
                ['git', 'ls-files'],
                cwd=folder_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                for file in result.stdout.strip().split('\n'):
                    if file:
                        ext = Path(file).suffix.lower()
                        if ext in extension_map:
                            extension_count[ext] += 1
        except Exception:
            pass
        return extension_count
    
    def check_package_json() -> ProgrammingLanguage:
        """Check for package.json to determine if it's a JavaScript/TypeScript project."""
        package_json_path = os.path.join(folder_path, 'package.json')
        if os.path.exists(package_json_path):
            try:
                import json
                with open(package_json_path, 'r') as f:
                    data = json.load(f)
                    # Check if it's a TypeScript project
                    deps = data.get('devDependencies', {})
                    if 'typescript' in deps or 'ts-node' in deps:
                        return ProgrammingLanguage.TYPESCRIPT
                    return ProgrammingLanguage.JAVASCRIPT
            except Exception:
                return ProgrammingLanguage.JAVASCRIPT
        return None
    
    if strategy == "package_json":
        result = check_package_json()
        if result:
            return result
        # Fall back to most_common if package.json not found
        strategy = "most_common"
    
    if strategy == "git_most_common":
        extension_count = get_git_files()
        if not extension_count:
            # Fall back to most_common if git fails
            extension_count = get_files_by_extension(folder_path)
    else:  # most_common
        extension_count = get_files_by_extension(folder_path)
    
    if extension_count:
        most_common_ext = extension_count.most_common(1)[0][0]
        return extension_map.get(most_common_ext, ProgrammingLanguage.UNKNOWN)
    
    return ProgrammingLanguage.UNKNOWN