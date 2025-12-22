import anthropic


def extract_text_blocks(blocks: Iterable[Any] | None) -> str:
    """
    Extract text from content blocks returned by Claude API.
    
    Args:
        blocks: An iterable of content blocks from Claude API response
        
    Returns:
        A string containing all text content from the blocks
    """
    if blocks is None:
        return ""
    
    text_parts = []
    for block in blocks:
        if hasattr(block, 'text'):
            text_parts.append(block.text)
    
    return "".join(text_parts)


if __name__ == "__main__":
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Say 'Hello, World!'"}
        ]
    )
    
    extracted_text = extract_text_blocks(message.content)
    print(f"Extracted text: {extracted_text}")