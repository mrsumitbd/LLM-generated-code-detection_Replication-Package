from dataclasses import dataclass, field

class TextFragment:
        """
        Represent a text fragment within a post with possibly additional styling.

        It also can contain a link to external resources (if link_data == None - it's just a text).
        """

        @dataclass
        class TextStyle:
            """Represent text styling options."""

            bold: bool = False
            italic: bool = False
            underline: bool = False

        text: str
        link_url: str | None = None
        header_level: int = 0  # Header level (0-6), 0 means no header
        style: TextStyle = field(default_factory=TextStyle)