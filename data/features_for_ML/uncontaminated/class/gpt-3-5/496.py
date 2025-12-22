from typing import List
from string import Template

class Lang:
    def __init__(self, name: str):
        self.name = name

class PromptUtils:
    """Utility class for loading and formatting prompts."""

    @staticmethod
    def load_prompt(filename: str) -> Template:
        with open(filename, 'r') as file:
            content = file.read()
        return Template(content)

    @staticmethod
    def format_context(context: List[str], question: str | None, lang: Lang) -> str:
        formatted_context = ', '.join(context)
        if question:
            return f"{formatted_context}. {question}"
        return formatted_context

    @staticmethod
    def get_full_language_name(lang: Lang) -> str:
        return lang.name