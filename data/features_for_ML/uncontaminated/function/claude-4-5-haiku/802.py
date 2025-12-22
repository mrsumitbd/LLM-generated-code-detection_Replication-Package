import anthropic


def extract_from_tag_block(txt: str, tag: str) -> str:
    """
    Extract content from a tag block in text using Claude API.
    
    Args:
        txt: The text containing the tag block
        tag: The tag name to extract content from
        
    Returns:
        The content extracted from the tag block
    """
    client = anthropic.Anthropic()
    
    prompt = f"""Extract the content from the <{tag}> tag block in the following text. 
Return only the content between the opening and closing tags, without the tags themselves.

Text:
{txt}"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text.strip()


if __name__ == "__main__":
    test_text = """
    <result>
    This is the extracted content
    </result>
    """
    
    result = extract_from_tag_block(test_text, "result")
    print(f"Extracted: {result}")