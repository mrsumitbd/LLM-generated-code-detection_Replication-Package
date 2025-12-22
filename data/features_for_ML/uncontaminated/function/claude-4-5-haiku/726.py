import anthropic


def _parse_from_test_patch(test_patch: str, func_name: str) -> str:
    """
    Parse a function implementation from a test patch using Claude.
    
    Args:
        test_patch: A string containing test code or patch information
        func_name: The name of the function to extract/implement
    
    Returns:
        A string containing the function implementation
    """
    client = anthropic.Anthropic()
    
    prompt = f"""Given the following test patch or test code:

{test_patch}

Please extract or implement the function named '{func_name}' based on the test requirements shown in the patch.
Return only the function implementation, starting with 'def {func_name}' and including the complete function body.
Do not include any explanations or additional text."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    test_patch_example = """
    def test_add():
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0
    """
    
    result = _parse_from_test_patch(test_patch_example, "add")
    print("Extracted function:")
    print(result)