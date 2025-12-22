import anthropic
import re


def path_to_regex(path: str) -> str:
    """
    Convert a path pattern to a regex pattern using Claude API.
    
    Args:
        path: A path pattern (e.g., "/users/:id/posts/:postId")
    
    Returns:
        A regex pattern string that matches the path pattern
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Convert the following path pattern to a regular expression pattern.
                
Path pattern: {path}

Rules:
- Replace :paramName with a regex group that captures any characters except /
- Keep literal parts of the path as-is
- The regex should match the entire path from start to end
- Return ONLY the regex pattern, nothing else

Example:
- Input: /users/:id
- Output: ^/users/([^/]+)$

- Input: /posts/:postId/comments/:commentId
- Output: ^/posts/([^/]+)/comments/([^/]+)$

Return only the regex pattern."""
            }
        ]
    )
    
    regex_pattern = message.content[0].text.strip()
    
    return regex_pattern


if __name__ == "__main__":
    test_paths = [
        "/users/:id",
        "/posts/:postId/comments/:commentId",
        "/api/v1/users/:userId/profile",
        "/files/:filename",
        "/search"
    ]
    
    for path in test_paths:
        regex = path_to_regex(path)
        print(f"Path: {path}")
        print(f"Regex: {regex}")
        print()