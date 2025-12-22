import anthropic


def make_code_text(files_dict, add_line_numbers=True):
    """
    Convert a dictionary of files into a formatted code text.
    
    Args:
        files_dict: Dictionary where keys are file paths and values are file contents
        add_line_numbers: Whether to add line numbers to the code
    
    Returns:
        A formatted string containing all files with optional line numbers
    """
    code_text = ""
    
    for file_path, content in files_dict.items():
        code_text += f"File: {file_path}\n"
        code_text += "=" * 50 + "\n"
        
        if add_line_numbers:
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                code_text += f"{i:4d} | {line}\n"
        else:
            code_text += content + "\n"
        
        code_text += "\n"
    
    return code_text


def analyze_code_with_claude(files_dict, query, add_line_numbers=True):
    """
    Analyze code files using Claude API.
    
    Args:
        files_dict: Dictionary where keys are file paths and values are file contents
        query: The question or analysis request for Claude
        add_line_numbers: Whether to add line numbers to the code
    
    Returns:
        Claude's analysis of the code
    """
    code_text = make_code_text(files_dict, add_line_numbers)
    
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Please analyze the following code:\n\n{code_text}\n\nQuery: {query}"
            }
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    # Example usage
    sample_files = {
        "main.py": "def hello():\n    print('Hello, World!')\n\nhello()",
        "utils.py": "def add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b"
    }
    
    # Test make_code_text
    formatted_code = make_code_text(sample_files, add_line_numbers=True)
    print("Formatted Code:")
    print(formatted_code)
    
    # Test with Claude
    analysis = analyze_code_with_claude(
        sample_files,
        "What does this code do? Are there any improvements you'd suggest?"
    )
    print("\nClaude's Analysis:")
    print(analysis)