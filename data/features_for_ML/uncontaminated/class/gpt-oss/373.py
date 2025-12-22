import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, ClassVar


@dataclass(eq=True, frozen=True)
class TodoItem:
    """
    Represents a single TODO item found in the codebase.

    Attributes
    ----------
    file_path : str
        Path to the file containing the TODO.
    line_number : int
        Line number where the TODO appears.
    text : str
        The text of the TODO comment.
    created_at : datetime
        Timestamp when the TodoItem instance was created.
    priority : Optional[int]
        Optional numeric priority extracted from the TODO text.
    """

    file_path: str
    line_number: int
    text: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    priority: Optional[int] = None

    # Regular expression to capture TODO comments and optional priority
    _TODO_RE: ClassVar[re.Pattern] = re.compile(
        r"""(?i)               # case-insensitive
            \bTODO\b           # the word TODO
            \s*                # optional whitespace
            (?:\((?P<pri>\d+)\))?   # optional priority in parentheses
            \s*[:\-]?\s*       # optional separator
            (?P<msg>.*)        # the rest of the message
        """,
        re.VERBOSE,
    )

    @classmethod
    def from_line(cls, file_path: str, line_number: int, line_text: str) -> Optional["TodoItem"]:
        """
        Parse a line of source code and return a TodoItem if a TODO is found.

        Parameters
        ----------
        file_path : str
            Path to the file containing the line.
        line_number : int
            The line number in the file.
        line_text : str
            The raw text of the line.

        Returns
        -------
        Optional[TodoItem]
            A TodoItem instance if a TODO comment is detected; otherwise None.
        """
        match = cls._TODO_RE.search(line_text)
        if not match:
            return None

        priority = match.group("pri")
        message = match.group("msg").strip()

        return cls(
            file_path=file_path,
            line_number=line_number,
            text=message,
            priority=int(priority) if priority is not None else None,
        )

    def __str__(self) -> str:
        """Human‑readable representation of the TODO item."""
        pri = f"({self.priority}) " if self.priority is not None else ""
        return f"{self.file_path}:{self.line_number}: TODO {pri}{self.text}"

    def to_dict(self) -> dict:
        """Return a dictionary representation suitable for JSON serialization."""
        return {
            "file_path": self.file_path,
            "line_number": self.line_number,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "priority": self.priority,
        }

    def __repr__(self) -> str:
        return (
            f"TodoItem(file_path={self.file_path!r}, "
            f"line_number={self.line_number!r}, text={self.text!r}, "
            f"priority={self.priority!r}, created_at={self.created_at!r})"
        )