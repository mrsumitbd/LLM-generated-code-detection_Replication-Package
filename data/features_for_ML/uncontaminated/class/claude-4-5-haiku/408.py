class TextFragment:
    """
    Represent a text fragment within a post with possibly additional styling.

    It also can contain a link to external resources (if link_data == None - it's just a text).
    """

    def __init__(self, text, bold=False, italic=False, underline=False, link_data=None):
        """
        Initialize a TextFragment.

        Args:
            text (str): The text content of the fragment
            bold (bool): Whether the text should be bold
            italic (bool): Whether the text should be italic
            underline (bool): Whether the text should be underlined
            link_data (dict or None): Link information if this fragment is a link
        """
        self.text = text
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.link_data = link_data

    def __repr__(self):
        """Return a string representation of the TextFragment."""
        return (f"TextFragment(text={self.text!r}, bold={self.bold}, "
                f"italic={self.italic}, underline={self.underline}, "
                f"link_data={self.link_data!r})")

    def __str__(self):
        """Return the text content of the fragment."""
        return self.text

    def __eq__(self, other):
        """Check equality with another TextFragment."""
        if not isinstance(other, TextFragment):
            return False
        return (self.text == other.text and
                self.bold == other.bold and
                self.italic == other.italic and
                self.underline == other.underline and
                self.link_data == other.link_data)

    def is_link(self):
        """Check if this fragment contains a link."""
        return self.link_data is not None

    def get_styled_text(self):
        """Return the text with styling markers."""
        result = self.text
        if self.bold:
            result = f"**{result}**"
        if self.italic:
            result = f"*{result}*"
        if self.underline:
            result = f"__{result}__"
        return result