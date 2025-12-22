from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Dict

# Try to import the real ClaudeCodeOptions if it exists.
try:
    from claude_code_options import ClaudeCodeOptions  # type: ignore
except Exception:  # pragma: no cover
    # Fallback minimal definition for testing purposes.
    @dataclass
    class ClaudeCodeOptions:
        builtin_permissions: bool = True
        continue_conversation: bool = False
        max_output_tokens: int = 1024
        temperature: float = 0.7
        top_p: float = 1.0
        stop_sequences: List[str] = field(default_factory=list)
        metadata: Dict[str, Any] = field(default_factory=dict)


def _create_default_claude_code_options(
    builtin_permissions: bool = True,
    continue_conversation: bool = False,
) -> ClaudeCodeOptions:
    """Create ClaudeCodeOptions with default values.

    Args:
        builtin_permissions: Whether to include built-in permission handling defaults
        continue_conversation: Whether to continue the conversation context
    """
    return ClaudeCodeOptions(
        builtin_permissions=builtin_permissions,
        continue_conversation=continue_conversation,
        max_output_tokens=1024,
        temperature=0.7,
        top_p=1.0,
        stop_sequences=[],
        metadata={},
    )