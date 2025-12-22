import anthropic


def fetch_genre(genre):
    """
    Fetch information about a given genre using Claude API.
    
    Args:
        genre: A string representing the genre to fetch information about
        
    Returns:
        A string containing information about the genre
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Tell me about the {genre} genre. Include its history, key characteristics, notable works, and influential artists."}
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    # Test the function with a few genres
    genres = ["jazz", "science fiction", "impressionism"]
    
    for genre in genres:
        print(f"\n{'='*60}")
        print(f"Genre: {genre.upper()}")
        print('='*60)
        result = fetch_genre(genre)
        print(result)