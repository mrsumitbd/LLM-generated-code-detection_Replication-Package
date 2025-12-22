import anthropic
import re


def get_soundcloud_track_id(url):
    """
    Extract the SoundCloud track ID from a given URL using Claude AI.
    
    Args:
        url: A SoundCloud URL string
        
    Returns:
        The track ID extracted from the URL, or None if not found
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Extract the SoundCloud track ID from this URL: {url}

SoundCloud URLs typically have formats like:
- https://soundcloud.com/artist/track-name
- https://soundcloud.com/artist/sets/playlist-name
- https://soundcloud.app.goog.gl/xxxxx (shortened URL)

The track ID is usually a numeric identifier. Please extract and return ONLY the track ID number, nothing else. If you cannot find a track ID, return "NOT_FOUND"."""
            }
        ]
    )
    
    response_text = message.content[0].text.strip()
    
    if response_text == "NOT_FOUND":
        return None
    
    # Try to extract numeric ID from the response
    numbers = re.findall(r'\d+', response_text)
    if numbers:
        return numbers[0]
    
    # If no numbers found, return the response as-is (might be an ID in other format)
    if response_text and response_text != "NOT_FOUND":
        return response_text
    
    return None


if __name__ == "__main__":
    # Test with a sample SoundCloud URL
    test_url = "https://soundcloud.com/artist/track-name"
    track_id = get_soundcloud_track_id(test_url)
    print(f"Track ID: {track_id}")