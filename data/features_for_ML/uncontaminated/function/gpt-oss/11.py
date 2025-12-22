def fetch_genre(genre):
    """
    Return basic information about a music genre.

    Parameters
    ----------
    genre : str
        The name of the genre to look up.

    Returns
    -------
    dict
        A dictionary containing a description and example artists for the genre.
    """
    genre = genre.lower()
    _genre_data = {
        "rock": {
            "description": "A genre of popular music that originated in the 1950s.",
            "examples": ["The Beatles", "Led Zeppelin", "Nirvana"],
        },
        "pop": {
            "description": "Popular music with catchy melodies and hooks.",
            "examples": ["Taylor Swift", "Ariana Grande", "Ed Sheeran"],
        },
        "jazz": {
            "description": "A genre characterized by swing, improvisation, and blue notes.",
            "examples": ["Miles Davis", "John Coltrane", "Ella Fitzgerald"],
        },
        "classical": {
            "description": "Music written in the Western classical tradition.",
            "examples": ["Ludwig van Beethoven", "Wolfgang Amadeus Mozart", "Johann Sebastian Bach"],
        },
        "hiphop": {
            "description": "A genre that includes rhythmic music and rap.",
            "examples": ["Kendrick Lamar", "Drake", "J. Cole"],
        },
        "country": {
            "description": "A genre of American folk music that evolved from ballads and dance tunes.",
            "examples": ["Johnny Cash", "Dolly Parton", "Garth Brooks"],
        },
        "electronic": {
            "description": "Music that primarily uses electronic instruments and technology.",
            "examples": ["Daft Punk", "Deadmau5", "Skrillex"],
        },
        "blues": {
            "description": "A genre that originated in African-American communities in the Deep South.",
            "examples": ["B.B. King", "Muddy Waters", "Robert Johnson"],
        },
        "reggae": {
            "description": "A music genre that originated in Jamaica in the late 1960s.",
            "examples": ["Bob Marley", "Peter Tosh", "Jimmy Cliff"],
        },
        "metal": {
            "description": "A genre of rock music that developed in the late 1960s and early 1970s.",
            "examples": ["Metallica", "Iron Maiden", "Black Sabbath"],
        },
    }

    return _genre_data.get(
        genre,
        {
            "description": "Unknown genre. No information available.",
            "examples": [],
        },
    )