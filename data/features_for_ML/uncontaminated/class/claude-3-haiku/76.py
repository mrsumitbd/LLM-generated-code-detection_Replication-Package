from typing import Union, List

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
        # Implement the logic to calculate the number of tokens for high-detail images
        return (width * height) // 1024

    def count_content(self, content: Union[str, List[Union[str, dict]]]) -> int:
        total_tokens = 0
        if isinstance(content, str):
            total_tokens += self.count_text(content)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, str):
                    total_tokens += self.count_text(item)
                elif isinstance(item, dict):
                    total_tokens += self.count_image(item)
        return total_tokens

    def count_tool_calls(self, tool_calls: List[dict]) -> int:
        total_tokens = 0
        for tool_call in tool_calls:
            total_tokens += self.count_content(tool_call.get('content', ''))
        return total_tokens

    def count_message_tokens(self, messages: List[dict]) -> int:
        total_tokens = 0
        for message in messages:
            total_tokens += self.count_content(message.get('content', ''))
        return total_tokens