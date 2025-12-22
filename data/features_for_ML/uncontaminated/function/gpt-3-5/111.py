def determine_project_language(folder_path: str, strategy: Literal["most_common", "git_most_common", "package_json"] = "git_most_common") -> ProgrammingLanguage:
    if strategy == "most_common":
        # Implement logic to determine language based on most common file extensions
        pass
    elif strategy == "git_most_common":
        # Implement logic to determine language based on files in the git repository
        pass
    elif strategy == "package_json":
        # Implement logic to determine language based on presence of package.json file
        pass