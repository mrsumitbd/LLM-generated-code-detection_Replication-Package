import anthropic
import json
from typing import Sequence


def find_token(token_list: Sequence[int], token: str) -> Sequence[int]:
    """
    Find all indices where a token appears in a token list using Claude's tokenizer.
    
    Args:
        token_list: A sequence of token IDs
        token: The text token to find
        
    Returns:
        A sequence of indices where the token appears in the token_list
    """
    client = anthropic.Anthropic()
    
    # Use Claude's tokenizer to get the token ID for the given text
    response = client.messages.tokenize(
        model="claude-3-5-sonnet-20241022",
        text=token
    )
    
    # Extract the token ID from the response
    token_ids = response.tokens
    
    # If the token produces multiple token IDs, we need to find sequences
    # For simplicity, we'll look for the first token ID
    if not token_ids:
        return []
    
    target_token_id = token_ids[0]
    
    # Find all indices where this token ID appears
    indices = []
    for i, t in enumerate(token_list):
        if t == target_token_id:
            indices.append(i)
    
    return indices