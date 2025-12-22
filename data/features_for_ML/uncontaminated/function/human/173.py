from graph_sitter.code_generation.enums import DocumentationDecorators
from graph_sitter.python.class_definition import PyClass
from graph_sitter.core.codebase import Codebase
from graph_sitter.shared.enums.programming_language import ProgrammingLanguage

def get_api_classes_by_decorator(
    codebase: Codebase,
    language: ProgrammingLanguage = ProgrammingLanguage.PYTHON,
) -> dict[str, PyClass]:
    """Returns all classes in a directory that have a specific decorator."""
    classes = {}
    language_specific_decorator = get_decorator_for_language(language).value
    general_decorator = DocumentationDecorators.GENERAL_API.value
    # get language specific classes
    for cls in codebase.classes:
        class_decorators = [decorator.name for decorator in cls.decorators]
        if language_specific_decorator in class_decorators:
            classes[cls.name] = cls
    for cls in codebase.classes:
        class_decorators = [decorator.name for decorator in cls.decorators]
        if general_decorator in class_decorators and cls.name not in classes.keys():
            classes[cls.name] = cls
    return classes