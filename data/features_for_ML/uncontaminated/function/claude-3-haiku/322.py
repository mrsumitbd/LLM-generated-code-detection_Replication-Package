def create_parser_for_language(
    language: Language, cast_config: CASTConfig | None = None
) -> LanguageParser:
    """Convenience function to create a parser for a language.

    Args:
        language: Programming language to create parser for
        cast_config: Optional cAST configuration

    Returns:
        LanguageParser instance configured for the language
    """
    if language == Language.PYTHON:
        return PythonParser(cast_config=cast_config)
    elif language == Language.JAVA:
        return JavaParser(cast_config=cast_config)
    elif language == Language.CPP:
        return CppParser(cast_config=cast_config)
    elif language == Language.JAVASCRIPT:
        return JavaScriptParser(cast_config=cast_config)
    else:
        raise ValueError(f"Unsupported language: {language}")