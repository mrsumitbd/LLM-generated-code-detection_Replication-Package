import re
from salmon.errors import GenreNotInWhitelist
from salmon.constants import GENRE_LIST

def fetch_genre(genre):
    normalized = normalize_accents(genre)
    key_search = re.sub(r"[^a-z]", "", normalized.lower().replace("&", "and"))
    try:
        return GENRE_LIST[key_search]
    except KeyError:
        raise GenreNotInWhitelist from None