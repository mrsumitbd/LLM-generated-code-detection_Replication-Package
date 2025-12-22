import anthropic
import os
import json


def load_book_content(setup: str, data_dir: str) -> str:
    """
    Load book content using Claude API with file handling.
    
    Args:
        setup: Setup instructions or context for loading the book
        data_dir: Directory containing the book data files
    
    Returns:
        The book content as a string
    """
    client = anthropic.Anthropic()
    
    # Read all files from the data directory
    files_content = {}
    if os.path.exists(data_dir):
        for filename in os.listdir(data_dir):
            filepath = os.path.join(data_dir, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        files_content[filename] = f.read()
                except (UnicodeDecodeError, IOError):
                    # Skip files that can't be read as text
                    pass
    
    # Prepare the prompt with file contents
    file_context = ""
    if files_content:
        file_context = "Available files:\n"
        for filename, content in files_content.items():
            file_context += f"\n--- File: {filename} ---\n{content}\n"
    
    prompt = f"""You are a book content loader. Your task is to load and process book content.

Setup instructions: {setup}

{file_context}

Based on the setup instructions and the available files, please load and return the book content. 
If there are multiple files, combine them appropriately. 
Return the complete book content as a single string."""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text