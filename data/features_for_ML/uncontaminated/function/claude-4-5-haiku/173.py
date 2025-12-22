def get_api_classes_by_decorator(
    codebase: Codebase,
    language: ProgrammingLanguage = ProgrammingLanguage.PYTHON,
) -> dict[str, PyClass]:
    """Returns all classes in a directory that have a specific decorator."""
    api_classes = {}
    
    if language != ProgrammingLanguage.PYTHON:
        return api_classes
    
    for file_path, file_content in codebase.files.items():
        if not file_path.endswith('.py'):
            continue
        
        try:
            tree = ast.parse(file_content)
        except SyntaxError:
            continue
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if class has decorators
                if node.decorator_list:
                    # Check for common API decorators
                    for decorator in node.decorator_list:
                        decorator_name = None
                        
                        if isinstance(decorator, ast.Name):
                            decorator_name = decorator.id
                        elif isinstance(decorator, ast.Attribute):
                            decorator_name = decorator.attr
                        elif isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Name):
                                decorator_name = decorator.func.id
                            elif isinstance(decorator.func, ast.Attribute):
                                decorator_name = decorator.func.attr
                        
                        # Check if it's an API-related decorator
                        if decorator_name and any(
                            api_keyword in decorator_name.lower()
                            for api_keyword in ['api', 'route', 'endpoint', 'resource']
                        ):
                            class_key = f"{file_path}:{node.name}"
                            py_class = PyClass(
                                name=node.name,
                                file_path=file_path,
                                decorators=[decorator_name],
                                lineno=node.lineno
                            )
                            api_classes[class_key] = py_class
                            break
    
    return api_classes