def create_parser_for_language(language: Language, cast_config: CASTConfig | None = None) -> LanguageParser:
    if cast_config is not None:
        return LanguageParser(language, cast_config)
    else:
        return LanguageParser(language)