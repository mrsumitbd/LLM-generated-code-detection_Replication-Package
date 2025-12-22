from typing import Optional
import contextvars

class PromptContext:
    _context_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar('prompt_context', default=None)

    def __init__(self):
        pass

    @property
    def _current_context(self) -> Optional[str]:
        return self._context_var.get()

    @_current_context.setter
    def _current_context(self, value: Optional[str]):
        self._context_var.set(value)