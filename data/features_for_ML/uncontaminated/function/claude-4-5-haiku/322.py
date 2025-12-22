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
    if cast_config is None:
        cast_config = CASTConfig()
    
    parser_map = {
        Language.PYTHON: PythonParser,
        Language.JAVA: JavaParser,
        Language.C: CParser,
        Language.CPP: CppParser,
        Language.JAVASCRIPT: JavaScriptParser,
        Language.TYPESCRIPT: TypeScriptParser,
        Language.GO: GoParser,
        Language.RUST: RustParser,
    }
    
    parser_class = parser_map.get(language)
    if parser_class is None:
        raise ValueError(f"Unsupported language: {language}")
    
    return parser_class(cast_config)