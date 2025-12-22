from typing import List, Tuple
import re

class ExpressionLearner:

    def __init__(self, chat_id: str) -> None:
        self.chat_id = chat_id
        self.learning_triggered = False
        self.message_count = 0

    def should_trigger_learning(self) -> bool:
        self.message_count += 1
        if self.message_count >= 10:
            self.learning_triggered = True
            self.message_count = 0
            return True
        return False

    def parse_expression_response(self, response: str) -> List[Tuple[str, str, str]]:
        expressions = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Match patterns like "expression | meaning | example"
            parts = [p.strip() for p in line.split('|')]
            
            if len(parts) >= 3:
                expression = parts[0]
                meaning = parts[1]
                example = parts[2]
                expressions.append((expression, meaning, example))
            elif len(parts) == 2:
                expression = parts[0]
                meaning = parts[1]
                expressions.append((expression, meaning, ""))
        
        return expressions

    def _build_bare_lines(self, messages: List) -> List[Tuple[int, str]]:
        bare_lines = []
        
        for idx, message in enumerate(messages):
            if isinstance(message, dict):
                text = message.get('text', '') or message.get('content', '')
            else:
                text = str(message)
            
            text = text.strip()
            
            if text:
                bare_lines.append((idx, text))
        
        return bare_lines