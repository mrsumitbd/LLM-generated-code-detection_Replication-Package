from difflib import SequenceMatcher as SM
from salmon import cfg

def dupe_check_recent_torrents(gazelle_site, searchstrs):
    """Checks the site log for recent uploads similar to ours.
    It may be a little slow as it has to fetch multiple pages of the log
    It also has to do a string distance comparison for each result"""
    searchstr = searchstrs[0]
    recent_uploads = gazelle_site.get_uploads_from_log()
    # Each upload in this list is best guess at (id,artist,title) from log
    hits = []
    seen = []
    for upload in recent_uploads:
        # We don't care about different torrents from the same release.
        torrent_str = upload[1] + upload[2]
        if torrent_str in seen:
            continue
        seen.append(torrent_str)
        artist = upload[1]
        title = upload[2]
        artist = [[artist, "main"]]
        possible_comparisons = generate_dupe_check_searchstrs(artist, title)
        ratio = 0
        for comparison_string in possible_comparisons:
            new_ratio = SM(None, searchstr, comparison_string).ratio()
            ratio = max(ratio, new_ratio)
        # Default tolerance is 0.5
        if ratio > cfg.upload.log_dupe_tolerance:
            hits.append(upload)
    return hits