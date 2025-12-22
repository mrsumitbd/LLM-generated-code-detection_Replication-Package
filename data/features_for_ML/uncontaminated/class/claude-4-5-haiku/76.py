class TokenCounter:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def count_text(self, text: str) -> int:
        tokens = self.tokenizer.encode(text)
        return len(tokens)

    def count_image(self, image_item: dict) -> int:
        if "url" in image_item:
            detail = image_item.get("detail", "auto")
        else:
            detail = image_item.get("detail", "auto")
        
        if detail == "low":
            return 85
        
        width = image_item.get("width", 1024)
        height = image_item.get("height", 1024)
        
        return self._calculate_high_detail_tokens(width, height)

    def _calculate_high_detail_tokens(self, width: int, height: int) -> int:
        max_dimension = 2048
        
        if width > max_dimension or height > max_dimension:
            scale = max_dimension / max(width, height)
            width = int(width * scale)
            height = int(height * scale)
        
        tiles_width = (width + 511) // 512
        tiles_height = (height + 511) // 512
        num_tiles = tiles_width * tiles_height
        
        tokens_per_tile = 170
        base_tokens = 85
        
        return base_tokens + num_tiles * tokens_per_tile

    def count_content(self, content: Union[str, List[Union[str, dict]]]) -> int:
        if isinstance(content, str):
            return self.count_text(content)
        
        total_tokens = 0
        if isinstance(content, list):
            for item in content:
                if isinstance(item, str):
                    total_tokens += self.count_text(item)
                elif isinstance(item, dict):
                    if item.get("type") == "text":
                        total_tokens += self.count_text(item.get("text", ""))
                    elif item.get("type") == "image_url":
                        total_tokens += self.count_image(item.get("image_url", {}))
        
        return total_tokens

    def count_tool_calls(self, tool_calls: List[dict]) -> int:
        total_tokens = 0
        for tool_call in tool_calls:
            if "function" in tool_call:
                func = tool_call["function"]
                if "name" in func:
                    total_tokens += self.count_text(func["name"])
                if "arguments" in func:
                    total_tokens += self.count_text(func["arguments"])
        
        return total_tokens

    def count_message_tokens(self, messages: List[dict]) -> int:
        total_tokens = 0
        
        for message in messages:
            if "content" in message:
                total_tokens += self.count_content(message["content"])
            
            if "tool_calls" in message:
                total_tokens += self.count_tool_calls(message["tool_calls"])
            
            if "role" in message:
                total_tokens += self.count_text(message["role"])
            
            if "name" in message:
                total_tokens += self.count_text(message["name"])
        
        return total_tokens