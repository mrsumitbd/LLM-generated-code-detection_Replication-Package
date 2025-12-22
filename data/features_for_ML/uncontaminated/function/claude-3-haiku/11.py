def fetch_genre(genre):
    genres = {
        "action": "Action",
        "comedy": "Comedy",
        "drama": "Drama",
        "horror": "Horror",
        "romance": "Romance",
        "sci-fi": "Science Fiction"
    }
    
    if genre.lower() in genres:
        return genres[genre.lower()]
    else:
        return "Unknown"