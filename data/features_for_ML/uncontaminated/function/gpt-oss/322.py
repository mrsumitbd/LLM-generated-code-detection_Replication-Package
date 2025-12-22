from __future__ import annotations

from typing import Optional

# Import the required types.  Adjust the import path if your project layout differs.
try:
    from cast import Language, CASTConfig, LanguageParser
except Exception:  # pragma: no cover
    # Fallback imports for environments where the cast package is not available.
    # These are minimal stubs to keep type checking happy; replace with real imports.
    class Language:  # pragma: no cover
        pass

    class CASTConfig:  # pragma: no cover
        pass

    class LanguageParser:  # pragma: no cover
        def __init__(self, language: Language, cast_config: CASTConfig | None = None):
            self.language = language
            self.cast_config = cast_config


def create_parser_for_language(
    language: Language,
    cast_config: Optional[CASTConfig] = None,
) -> LanguageParser:
    """
    Convenience function to create a parser for a language.

    Args:
        language: Programming language to create parser for
        cast_config: Optional cAST configuration

    Returns:
        LanguageParser instance configured for the language
    """
    # If no configuration is supplied, use the default CASTConfig.
    if cast_config is None:
        cast_config = CASTConfig()

    # Instantiate and return the LanguageParser.
    return LanguageParser(language, cast_config)