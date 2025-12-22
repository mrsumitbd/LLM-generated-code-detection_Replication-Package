from typing import List, Union

class TokenCounter:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def count_text(self, text: str) -> int:
        tokens = self.tokenizer.tokenize(text)
        return len(tokens)

    def count_image(self, image_item: dict) -> int:
        width = image_item.get('width', 0)
        height = image_item.get('height', 0)
        return self._calculate_high_detail_tokens(width, height)

    def _calculate_high_detail_tokens(self, width: int, height: int) -> int:
        return width * height

    def count_content(self, content: Union[str, List[Union[str, dict]]]) -> int:
        if isinstance(content, str):
            return self.count_text(content)
        elif isinstance(content, list):
            total_tokens = 0
            for item in content:
                if isinstance(item, str):
                    total_tokens += self.count_text(item)
                elif isinstance(item, dict):
                    total_tokens += self.count_image(item)
            return total_tokens
        return 0

    def count_tool_calls(self, tool_calls: List[dict]) -> int:
        total_tokens = 0
        for call in tool_calls:
            if 'content' in call:
                total_tokens += self.count_content(call['content'])
        return total_tokens

    def count_message_tokens(self, messages: List[dict]) -> int:
        total_tokens = 0
        for message in messages:
            if 'tools' in message:
                total_tokens += self.count_tool_calls(message['tools'])
        return total_tokens