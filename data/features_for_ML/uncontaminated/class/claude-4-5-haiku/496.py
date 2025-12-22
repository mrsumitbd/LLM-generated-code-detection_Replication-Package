from string import Template
from enum import Enum
from pathlib import Path


class Lang(Enum):
    EN = "en"
    ES = "es"
    FR = "fr"
    DE = "de"
    IT = "it"
    PT = "pt"
    JA = "ja"
    ZH = "zh"
    RU = "ru"
    KO = "ko"


class PromptUtils:
    """Utility class for loading and formatting prompts."""

    _LANGUAGE_NAMES = {
        Lang.EN: "English",
        Lang.ES: "Spanish",
        Lang.FR: "French",
        Lang.DE: "German",
        Lang.IT: "Italian",
        Lang.PT: "Portuguese",
        Lang.JA: "Japanese",
        Lang.ZH: "Chinese",
        Lang.RU: "Russian",
        Lang.KO: "Korean",
    }

    @staticmethod
    def load_prompt(filename: str) -> Template:
        """Load a prompt template from a file."""
        prompt_dir = Path(__file__).parent / "prompts"
        filepath = prompt_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Prompt file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return Template(content)

    @staticmethod
    def format_context(context: list[str], question: str | None, lang: Lang) -> str:
        """Format context and question into a structured string."""
        formatted_parts = []
        
        if context:
            formatted_parts.append("Context:")
            for i, item in enumerate(context, 1):
                formatted_parts.append(f"{i}. {item}")
        
        if question:
            formatted_parts.append(f"\nQuestion ({PromptUtils.get_full_language_name(lang)}):")
            formatted_parts.append(question)
        
        return "\n".join(formatted_parts)

    @staticmethod
    def get_full_language_name(lang: Lang) -> str:
        """Get the full language name from a Lang enum value."""
        return PromptUtils._LANGUAGE_NAMES.get(lang, lang.value)