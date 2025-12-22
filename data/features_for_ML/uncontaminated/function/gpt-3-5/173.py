def get_api_classes_by_decorator(
    codebase: Codebase,
    language: ProgrammingLanguage = ProgrammingLanguage.PYTHON,
) -> dict[str, PyClass]:
    api_classes = {}
    for file in codebase.files:
        if file.language == language:
            for class_name, py_class in file.classes.items():
                if py_class.has_decorator("api"):
                    api_classes[class_name] = py_class
    return api_classes