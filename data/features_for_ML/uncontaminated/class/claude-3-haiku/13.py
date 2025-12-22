from typing import List, Tuple

class ExpressionLearner:

    def __init__(self, chat_id: str) -> None:
        self.chat_id = chat_id
        self.expression_responses = []

    def should_trigger_learning(self) -> bool:
        return len(self.expression_responses) >= 3

    def parse_expression_response(self, response: str) -> List[Tuple[str, str, str]]:
        expressions = []
        lines = response.split('\n')
        for line in lines:
            parts = line.split(' = ')
            if len(parts) == 2:
                expression, result = parts
                expressions.append((expression.strip(), '=', result.strip()))
        return expressions

    def _build_bare_lines(self, messages: List) -> List[Tuple[int, str]]:
        bare_lines = []
        for i, message in enumerate(messages):
            if message.startswith('/learn'):
                continue
            bare_lines.append((i, message))
        return bare_lines