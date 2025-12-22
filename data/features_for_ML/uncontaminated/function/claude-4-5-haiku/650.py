import anthropic


def sanitize_path(path: str) -> str:
    """
    Sanitize a file path to prevent directory traversal attacks.
    Uses Claude to analyze and sanitize the path.
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Sanitize the following file path to prevent directory traversal attacks. 
Remove any ".." sequences, leading slashes, and other potentially dangerous patterns.
Return ONLY the sanitized path, nothing else.

Path to sanitize: {path}"""
            }
        ]
    )
    
    sanitized = message.content[0].text.strip()
    return sanitized


if __name__ == "__main__":
    test_paths = [
        "../../../etc/passwd",
        "../../sensitive/file.txt",
        "/etc/passwd",
        "normal/path/to/file.txt",
        "./current/dir/file.txt",
        "path/../../../etc/passwd",
        "...//...//etc/passwd"
    ]
    
    for test_path in test_paths:
        result = sanitize_path(test_path)
        print(f"Original: {test_path}")
        print(f"Sanitized: {result}")
        print()