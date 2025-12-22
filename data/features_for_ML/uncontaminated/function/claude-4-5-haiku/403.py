import anthropic
import json


def get_random_audiobook_covers_with_links():
    """
    Generate random audiobook covers with links using Claude's vision capabilities.
    Returns a list of audiobook cover descriptions with associated links.
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": """Generate a JSON array of 5 random audiobook covers with the following structure for each:
{
    "title": "Book title",
    "author": "Author name",
    "cover_description": "Detailed description of what the cover looks like",
    "genre": "Genre",
    "link": "A plausible audiobook link (e.g., audible.com, scribd.com, etc.)"
}

Make the covers diverse in style and genre. Return only valid JSON array, no other text."""
            }
        ]
    )
    
    response_text = message.content[0].text
    audiobook_covers = json.loads(response_text)
    
    return audiobook_covers


if __name__ == "__main__":
    covers = get_random_audiobook_covers_with_links()
    print(json.dumps(covers, indent=2))