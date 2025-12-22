import difflib
from typing import List, Dict, Any

def dupe_check_recent_torrents(gazelle_site, searchstrs: List[str]) -> List[Dict[str, Any]]:
    """
    Checks the site log for recent uploads similar to the supplied search strings.
    The function iterates over all available log pages, compares each entry's title
    to each search string using a similarity ratio, and collects entries that
    exceed a similarity threshold.

    Parameters
    ----------
    gazelle_site : object
        An object representing the gazelle site. It must provide a method
        `get_recent_uploads(page: int) -> List[Dict[str, Any]]` that returns
        a list of upload entries for the given page. Each entry should
        contain at least a 'title' key.
    searchstrs : List[str]
        A list of strings to compare against the titles in the log.

    Returns
    -------
    List[Dict[str, Any]]
        A list of log entries that are considered duplicates. Each entry
        is the dictionary returned by `get_recent_uploads`.
    """
    # Threshold for considering two strings similar.
    SIMILARITY_THRESHOLD = 0.8

    duplicates: List[Dict[str, Any]] = []
    page = 1

    while True:
        try:
            entries = gazelle_site.get_recent_uploads(page)
        except Exception:
            # If the site raises an error (e.g., network issue), stop searching.
            break

        if not entries:
            # No more entries to process.
            break

        for entry in entries:
            title = entry.get("title", "")
            if not title:
                continue

            title_lower = title.lower()
            for search in searchstrs:
                search_lower = search.lower()
                ratio = difflib.SequenceMatcher(None, title_lower, search_lower).ratio()
                if ratio >= SIMILARITY_THRESHOLD:
                    duplicates.append(entry)
                    # Stop checking other search strings for this entry.
                    break

        page += 1

    return duplicates