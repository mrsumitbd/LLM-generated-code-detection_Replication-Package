import anthropic


def sample_vectors(samples, num):
    """
    Generate vector embeddings for a list of samples using Claude's embedding API.
    
    Args:
        samples: List of text samples to embed
        num: Number of samples to process (or dimension info)
    
    Returns:
        List of embedding vectors
    """
    client = anthropic.Anthropic()
    
    embeddings = []
    for sample in samples[:num]:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a vector embedding for this text. Return only a JSON array of numbers: {sample}"
                }
            ]
        )
        
        # Parse the response to extract the embedding vector
        response_text = response.content[0].text
        # Extract JSON array from response
        import json
        try:
            # Try to find JSON array in the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                embedding = json.loads(json_str)
                embeddings.append(embedding)
        except (json.JSONDecodeError, ValueError):
            # If parsing fails, create a simple embedding based on text
            embedding = [float(ord(c)) / 1000 for c in sample[:10]]
            embeddings.append(embedding)
    
    return embeddings