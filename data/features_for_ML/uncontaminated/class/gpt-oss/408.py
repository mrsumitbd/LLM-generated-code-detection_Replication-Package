from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class TextFragment:
    """
    Represent a text fragment within a post with possibly additional styling.

    It also can contain a link to external resources (if link_data == None - it's just a text).
    """

    text: str
    style: Dict[str, Any] = field(default_factory=dict)
    link_data: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not isinstance(self.text, str):
            raise TypeError("text must be a string")
        if not isinstance(self.style, dict):
            raise TypeError("style must be a dict")
        if self.link_data is not None and not isinstance(self.link_data, dict):
            raise TypeError("link_data must be a dict or None")

    # ------------------------------------------------------------------
    # Basic helpers
    # ------------------------------------------------------------------
    def is_link(self) -> bool:
        """Return True if the fragment contains a link."""
        return self.link_data is not None

    def plain_text(self) -> str:
        """Return the raw text without any styling or link markup."""
        return self.text

    def __len__(self) -> int:
        return len(self.text)

    # ------------------------------------------------------------------
    # Rendering helpers
    # ------------------------------------------------------------------
    def to_html(self) -> str:
        """Return an HTML representation of the fragment."""
        s = self.text

        # Apply inline styles
        if self.style.get("bold"):
            s = f"<b>{s}</b>"
        if self.style.get("italic"):
            s = f"<i>{s}</i>"
        if self.style.get("underline"):
            s = f"<u>{s}</u>"
        if color := self.style.get("color"):
            s = f'<span style="color:{color}">{s}</span>'

        # Wrap with link if present
        if self.is_link():
            url = self.link_data.get("url", "#")
            title = self.link_data.get("title", "")
            target = self.link_data.get("target", "_blank")
            s = f'<a href="{url}" title="{title}" target="{target}">{s}</a>'

        return s

    def to_markdown(self) -> str:
        """Return a Markdown representation of the fragment."""
        s = self.text

        # Apply Markdown styles
        if self.style.get("bold"):
            s = f"**{s}**"
        if self.style.get("italic"):
            s = f"*{s}*"
        if self.style.get("underline"):
            # Markdown doesn't support underline; use HTML fallback
            s = f"<u>{s}</u>"

        # Wrap with link if present
        if self.is_link():
            url = self.link_data.get("url", "#")
            title = self.link_data.get("title", "")
            title_part = f' "{title}"' if title else ""
            s = f"[{s}]({url}{title_part})"

        return s

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable dictionary representation."""
        return {
            "text": self.text,
            "style": dict(self.style),
            "link_data": dict(self.link_data) if self.link_data else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TextFragment":
        """Create a TextFragment from a dictionary."""
        return cls(
            text=data.get("text", ""),
            style=data.get("style", {}),
            link_data=data.get("link_data"),
        )

    def copy(self, **updates) -> "TextFragment":
        """Return a copy of the fragment with optional updates."""
        new_kwargs = {
            "text": self.text,
            "style": dict(self.style),
            "link_data": dict(self.link_data) if self.link_data else None,
        }
        new_kwargs.update(updates)
        return TextFragment(**new_kwargs)

    def apply_style(self, **style_updates) -> "TextFragment":
        """Return a new fragment with updated style."""
        new_style = dict(self.style)
        new_style.update(style_updates)
        return self.copy(style=new_style)

    def merge_with(self, other: "TextFragment") -> Optional["TextFragment"]:
        """
        Merge with another fragment if they share the same style and link_data.
        Returns a new TextFragment or None if they cannot be merged.
        """
        if not isinstance(other, TextFragment):
            return None
        if self.style != other.style or self.link_data != other.link_data:
            return None
        return TextFragment(
            text=self.text + other.text,
            style=self.style,
            link_data=self.link_data,
        )

    # ------------------------------------------------------------------
    # Representation helpers
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"TextFragment(text={self.text!r}, "
            f"style={self.style!r}, link_data={self.link_data!r})"
        )

    def __str__(self) -> str:
        return self.plain_text()