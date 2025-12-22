from typing import List, Tuple, Any


class ExpressionLearner:
    """
    A simple expression learning helper.

    The class keeps track of a chat session identified by ``chat_id`` and
    provides utilities for deciding when to trigger learning, parsing
    responses that contain expressions, and extracting bare lines from
    a list of messages.
    """

    def __init__(self, chat_id: str) -> None:
        """
        Initialise the learner with a chat identifier.

        Parameters
        ----------
        chat_id : str
            Unique identifier for the chat session.
        """
        self.chat_id = chat_id
        self._message_count = 0
        self._learning_threshold = 5  # arbitrary threshold for demo

    def should_trigger_learning(self) -> bool:
        """
        Decide whether the learner should trigger a learning phase.

        Returns
        -------
        bool
            ``True`` if the number of messages processed so far exceeds
            the learning threshold, otherwise ``False``.
        """
        self._message_count += 1
        return self._message_count >= self._learning_threshold

    def parse_expression_response(self, response: str) -> List[Tuple[str, str, str]]:
        """
        Parse a response string that contains expressions.

        The expected format for each line is:
            expression - meaning; example

        The example part is optional. Lines that do not match the format
        are ignored.

        Parameters
        ----------
        response : str
            Multiline string containing expressions.

        Returns
        -------
        List[Tuple[str, str, str]]
            A list of tuples where each tuple contains
            (expression, meaning, example).
        """
        parsed: List[Tuple[str, str, str]] = []
        for line in response.splitlines():
            line = line.strip()
            if not line:
                continue
            # Split into expression and the rest
            if " - " not in line:
                continue
            expr, rest = line.split(" - ", 1)
            expr = expr.strip()
            # Split meaning and optional example
            if ";" in rest:
                meaning, example = rest.split(";", 1)
                meaning = meaning.strip()
                example = example.strip()
            else:
                meaning = rest.strip()
                example = ""
            parsed.append((expr, meaning, example))
        return parsed

    def _build_bare_lines(self, messages: List[Any]) -> List[Tuple[int, str]]:
        """
        Convert a list of message objects into a list of (index, content) tuples.

        Parameters
        ----------
        messages : List[Any]
            A list where each element is expected to have a ``content`` attribute
            or be a string. If an element is a dict, the ``content`` key is used.

        Returns
        -------
        List[Tuple[int, str]]
            A list of tuples containing the message index and its textual content.
        """
        bare_lines: List[Tuple[int, str]] = []
        for idx, msg in enumerate(messages):
            if isinstance(msg, str):
                content = msg
            elif isinstance(msg, dict):
                content = msg.get("content", "")
            else:
                # Fallback: use str representation
                content = str(msg)
            bare_lines.append((idx, content))
        return bare_lines