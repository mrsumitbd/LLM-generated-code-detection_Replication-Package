from typing import Union, List, Dict

class TokenCounter:
    """
    A simple token counter that works with a tokenizer that implements an `encode` method.
    It can count tokens for text, images, content lists, tool calls, and messages.
    """

    def __init__(self, tokenizer):
        """
        :param tokenizer: An object with an `encode(text: str) -> List[int]` method.
        """
        self.tokenizer = tokenizer

    def count_text(self, text: str) -> int:
        """
        Count tokens in a plain text string.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return len(self.tokenizer.encode(text))

    def count_image(self, image_item: Dict) -> int:
        """
        Count tokens for an image represented as a dict.
        Expected keys: 'width', 'height'.
        """
        width = image_item.get("width")
        height = image_item.get("height")
        if width is None or height is None:
            raise ValueError("image_item must contain 'width' and 'height'")
        return self._calculate_high_detail_tokens(width, height)

    def _calculate_high_detail_tokens(self, width: int, height: int) -> int:
        """
        Estimate token count for an image based on its resolution.
        The formula is a simplified approximation: one token per 512 pixels.
        """
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive integers")
        pixels = width * height
        # One token per 512 pixels, rounded up
        return (pixels + 511) // 512

    def count_content(self, content: Union[str, List[Union[str, Dict]]]) -> int:
        """
        Count tokens in content that can be a string or a list of strings/dicts.
        """
        if isinstance(content, str):
            return self.count_text(content)
        if isinstance(content, list):
            total = 0
            for item in content:
                if isinstance(item, str):
                    total += self.count_text(item)
                elif isinstance(item, dict):
                    total += self.count_image(item)
                else:
                    raise TypeError(f"Unsupported content item type: {type(item)}")
            return total
        raise TypeError(f"Unsupported content type: {type(content)}")

    def count_tool_calls(self, tool_calls: List[Dict]) -> int:
        """
        Count tokens in a list of tool call dictionaries.
        Each tool call may contain a 'function' key with 'arguments' string.
        """
        total = 0
        for call in tool_calls:
            if not isinstance(call, dict):
                raise TypeError("Each tool call must be a dict")
            # Count arguments if present
            func = call.get("function")
            if isinstance(func, dict):
                args = func.get("arguments")
                if isinstance(args, str):
                    total += self.count_text(args)
            # Count any other string fields
            for key, value in call.items():
                if isinstance(value, str):
                    total += self.count_text(value)
        return total

    def count_message_tokens(self, messages: List[Dict]) -> int:
        """
        Count tokens for a list of message dictionaries.
        Each message may contain 'content' and/or 'tool_calls'.
        """
        total = 0
        for msg in messages:
            if not isinstance(msg, dict):
                raise TypeError("Each message must be a dict")
            # Count content
            content = msg.get("content")
            if content is not None:
                total += self.count_content(content)
            # Count tool calls
            tool_calls = msg.get("tool_calls")
            if isinstance(tool_calls, list):
                total += self.count_tool_calls(tool_calls)
        return total