from typing import Any, Callable, List, Mapping, Optional, Sequence

class _LogConfig:
    """Parsed configuration from PYTHON_LOG: default level and per-pattern rules."""

    default_level_name: str
    rules: Sequence[_Rule]