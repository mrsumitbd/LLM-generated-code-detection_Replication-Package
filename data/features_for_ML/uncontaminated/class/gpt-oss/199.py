import re
from typing import Callable, List, Tuple, Any


class MessageValidator:
    """
    A simple message validator that supports a set of validation rules.
    Each rule is a callable that receives the message and returns a tuple
    (bool, str) where the bool indicates success and the str is an error
    message if the rule fails.
    """

    def __init__(self):
        # Default rules: non-empty string, length <= 200, no disallowed words
        self._rules: List[Callable[[Any], Tuple[bool, str]]] = []

        # Rule: message must be a string
        def rule_is_string(msg):
            if not isinstance(msg, str):
                return False, "Message must be a string."
            return True, ""

        # Rule: message must not be empty or whitespace only
        def rule_non_empty(msg):
            if msg.strip() == "":
                return False, "Message cannot be empty."
            return True, ""

        # Rule: message length <= 200
        def rule_length(msg):
            if len(msg) > 200:
                return False, "Message exceeds maximum length of 200 characters."
            return True, ""

        # Rule: no disallowed words (example: profanity filter)
        disallowed_words = {"badword", "anotherbadword"}
        def rule_no_disallowed(msg):
            words = set(re.findall(r"\b\w+\b", msg.lower()))
            if words & disallowed_words:
                return False, f"Message contains disallowed words: {words & disallowed_words}"
            return True, ""

        self._rules.extend([rule_is_string, rule_non_empty, rule_length, rule_no_disallowed])

    def add_rule(self, rule: Callable[[Any], Tuple[bool, str]]) -> None:
        """
        Add a custom validation rule.
        The rule must accept a single argument (the message) and return
        a tuple (bool, str) where bool indicates success and str is an error
        message if the rule fails.
        """
        if not callable(rule):
            raise TypeError("Rule must be callable.")
        self._rules.append(rule)

    def validate(self, message: Any) -> None:
        """
        Validate the message against all rules.
        Raises ValueError with the first encountered error message if validation fails.
        """
        for rule in self._rules:
            ok, err = rule(message)
            if not ok:
                raise ValueError(err)

    def is_valid(self, message: Any) -> bool:
        """
        Return True if the message passes all validation rules, False otherwise.
        """
        try:
            self.validate(message)
            return True
        except ValueError:
            return False

    def get_errors(self, message: Any) -> List[str]:
        """
        Return a list of error messages for all failing rules.
        """
        errors = []
        for rule in self._rules:
            ok, err = rule(message)
            if not ok:
                errors.append(err)
        return errors