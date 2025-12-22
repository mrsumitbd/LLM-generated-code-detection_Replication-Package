from chunkhound.core.types.common import Language
from chunkhound.interfaces.language_parser import LanguageParser
from chunkhound.parsers.universal_parser import CASTConfig, UniversalParser
from tree_sitter import Language

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
    factory = get_parser_factory(cast_config)
    return factory.create_parser(language, cast_config)