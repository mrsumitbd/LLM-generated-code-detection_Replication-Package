def get_api_classes_by_decorator(
    codebase: Codebase,
    language: ProgrammingLanguage = ProgrammingLanguage.PYTHON,
) -> dict[str, PyClass]:
    """Returns all classes in a directory that have a specific decorator."""
    api_classes = {}
    for file_path in codebase.get_files(language=language):
        for class_obj in codebase.get_classes(file_path, language=language):
            if any(decorator.name == "api" for decorator in class_obj.decorators):
                api_classes[class_obj.name] = class_obj
    return api_classes