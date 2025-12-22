from typing import Optional

class PromptContext:
    def __init__(self):
        self._context: Optional[str] = None

    @property
    def _current_context(self) -> Optional[str]:
        return self._context

    @_current_context.setter
    def _current_context(self, value: Optional[str]):
        self._context = value