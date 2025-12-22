import anthropic


def lcs_similarity(string1, string2):
    """
    Calculate the similarity between two strings using Longest Common Subsequence (LCS).
    Uses Claude to compute the LCS and return a similarity score.
    
    Args:
        string1: First string to compare
        string2: Second string to compare
    
    Returns:
        A similarity score between 0 and 1, where 1 means identical strings
    """
    client = anthropic.Anthropic()
    
    prompt = f"""Calculate the Longest Common Subsequence (LCS) similarity between these two strings:

String 1: "{string1}"
String 2: "{string2}"

Please:
1. Find the longest common subsequence
2. Calculate the similarity score as: 2 * len(LCS) / (len(string1) + len(string2))
3. Return ONLY a JSON object with this format:
{{"lcs": "the_lcs_string", "similarity": 0.0}}

Where similarity is a float between 0 and 1."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text
    
    import json
    result = json.loads(response_text)
    
    return result["similarity"]