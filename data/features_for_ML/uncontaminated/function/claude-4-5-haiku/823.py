import anthropic
import json
from typing import List, Dict


def build_search_index(messages: List[Dict], patterns: List[Dict], errors: List[Dict]) -> str:
    """
    Build 500-token search index optimized for keyword matching.

    Opus structure:
    - User request (exact words)
    - Solution type + tools used
    - Files modified + operation types
    - Primary keywords (3-5 specific terms)
    """
    client = anthropic.Anthropic()
    
    # Prepare the context for Claude
    messages_text = json.dumps(messages, indent=2)
    patterns_text = json.dumps(patterns, indent=2)
    errors_text = json.dumps(errors, indent=2)
    
    prompt = f"""Analyze the following conversation, patterns, and errors to build a search index.

MESSAGES:
{messages_text}

PATTERNS:
{patterns_text}

ERRORS:
{errors_text}

Create a 500-token search index with this structure:
1. User request (extract exact words from the user's main request)
2. Solution type + tools used (identify what type of solution was provided and what tools/technologies were used)
3. Files modified + operation types (list files that were modified and the types of operations performed)
4. Primary keywords (3-5 specific, searchable terms that capture the essence of this interaction)

Format the index as a clear, structured text that can be used for keyword matching and search optimization."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the search index from the response
    search_index = message.content[0].text
    
    return search_index


if __name__ == "__main__":
    # Example usage
    sample_messages = [
        {"role": "user", "content": "How do I implement a binary search tree in Python?"},
        {"role": "assistant", "content": "Here's a complete implementation of a binary search tree..."}
    ]
    
    sample_patterns = [
        {"pattern": "data structure", "frequency": 3},
        {"pattern": "tree traversal", "frequency": 2}
    ]
    
    sample_errors = [
        {"error": "None", "context": "No errors encountered"}
    ]
    
    index = build_search_index(sample_messages, sample_patterns, sample_errors)
    print("Search Index:")
    print(index)