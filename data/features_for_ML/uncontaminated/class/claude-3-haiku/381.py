from typing import Optional

class PromptContext:
    def __init__(self):
        self._current_context = None

    @property
    def _current_context(self) -> Optional[str]:
        return self._current_context

    @_current_context.setter
    def _current_context(self, value: Optional[str]):
        self._current_context = value