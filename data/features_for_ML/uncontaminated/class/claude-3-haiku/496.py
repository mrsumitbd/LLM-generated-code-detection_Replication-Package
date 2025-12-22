from string import Template

class Lang(str):
    """Enum-like class for language codes."""
    ENGLISH = "en"
    FRENCH = "fr"
    GERMAN = "de"

class PromptUtils:
    """Utility class for loading and formatting prompts."""

    @staticmethod
    def load_prompt(filename: str) -> Template:
        with open(filename, "r") as file:
            prompt_template = Template(file.read())
        return prompt_template

    @staticmethod
    def format_context(context: list[str], question: str | None, lang: Lang) -> str:
        full_lang_name = PromptUtils.get_full_language_name(lang)
        context_str = "\n".join(context)
        if question:
            return f"Context ({full_lang_name}):\n{context_str}\n\nQuestion: {question}"
        else:
            return f"Context ({full_lang_name}):\n{context_str}"

    @staticmethod
    def get_full_language_name(lang: Lang) -> str:
        if lang == Lang.ENGLISH:
            return "English"
        elif lang == Lang.FRENCH:
            return "French"
        elif lang == Lang.GERMAN:
            return "German"
        else:
            return "Unknown"