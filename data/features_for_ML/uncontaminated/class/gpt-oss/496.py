import pathlib
from string import Template
from typing import List, Optional, Union

try:
    # If a Lang enum is defined elsewhere, import it
    from .lang import Lang  # type: ignore
except Exception:
    # Fallback: define a minimal Lang placeholder for type checking
    from enum import Enum

    class Lang(Enum):
        EN = "en"
        FR = "fr"
        ES = "es"
        DE = "de"
        ZH = "zh"
        JA = "ja"
        RU = "ru"
        PT = "pt"
        IT = "it"
        KO = "ko"


class PromptUtils:
    """Utility class for loading and formatting prompts."""

    @staticmethod
    def load_prompt(filename: str) -> Template:
        """
        Load a prompt template from a file.

        Parameters
        ----------
        filename : str
            Path to the prompt file.

        Returns
        -------
        Template
            A string.Template instance containing the prompt.
        """
        path = pathlib.Path(filename)
        if not path.is_file():
            raise FileNotFoundError(f"Prompt file not found: {filename}")
        content = path.read_text(encoding="utf-8")
        return Template(content)

    @staticmethod
    def format_context(
        context: List[str], question: Optional[str], lang: Union[Lang, str]
    ) -> str:
        """
        Format a list of context strings, an optional question, and a language
        into a single prompt string.

        Parameters
        ----------
        context : List[str]
            List of context lines.
        question : Optional[str]
            The question to ask, if any.
        lang : Union[Lang, str]
            The language code or Lang enum.

        Returns
        -------
        str
            The formatted context string.
        """
        # Join context lines
        ctx = "\n".join(context)

        # Append question if provided
        if question:
            ctx += f"\n\nQuestion: {question}"

        # Append language information
        full_lang = PromptUtils.get_full_language_name(lang)
        ctx += f"\n\nLanguage: {full_lang}"

        return ctx

    @staticmethod
    def get_full_language_name(lang: Union[Lang, str]) -> str:
        """
        Convert a language code or Lang enum to its full language name.

        Parameters
        ----------
        lang : Union[Lang, str]
            Language code or Lang enum.

        Returns
        -------
        str
            Full language name.
        """
        # Mapping of common language codes to full names
        mapping = {
            "en": "English",
            "fr": "French",
            "es": "Spanish",
            "de": "German",
            "zh": "Chinese",
            "ja": "Japanese",
            "ru": "Russian",
            "pt": "Portuguese",
            "it": "Italian",
            "ko": "Korean",
        }

        # If lang is an Enum, try to get its value
        if hasattr(lang, "value"):
            code = str(lang.value).lower()
        else:
            code = str(lang).lower()

        return mapping.get(code, code.capitalize())