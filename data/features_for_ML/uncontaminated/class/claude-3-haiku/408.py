class TextFragment:
    """
    Represent a text fragment within a post with possibly additional styling.

    It also can contain a link to external resources (if link_data == None - it's just a text).
    """

    def __init__(self, text, link_data=None, bold=False, italic=False, underline=False):
        self.text = text
        self.link_data = link_data
        self.bold = bold
        self.italic = italic
        self.underline = underline

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"TextFragment('{self.text}', {self.link_data}, {self.bold}, {self.italic}, {self.underline})"

    def apply_style(self, text):
        styled_text = text
        if self.bold:
            styled_text = f"**{styled_text}**"
        if self.italic:
            styled_text = f"*{styled_text}*"
        if self.underline:
            styled_text = f"__{styled_text}__"
        if self.link_data:
            styled_text = f"[{styled_text}]({self.link_data})"
        return styled_text