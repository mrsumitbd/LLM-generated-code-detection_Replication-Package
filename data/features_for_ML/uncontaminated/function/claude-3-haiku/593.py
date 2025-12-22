import requests
from fuzzywuzzy import fuzz

def dupe_check_recent_torrents(gazelle_site, searchstrs):
    """Checks the site log for recent uploads similar to ours.
    It may be a little slow as it has to fetch multiple pages of the log
    It also has to do a string distance comparison for each result"""
    results = []
    page = 1
    while True:
        url = f"{gazelle_site}/torrents.php?page={page}&order=time&direction=desc"
        response = requests.get(url)
        if "No results found" in response.text:
            break
        for line in response.text.split("\n"):
            if "torrent.php?id=" in line:
                torrent_id = line.split("torrent.php?id=")[1].split("&")[0]
                for searchstr in searchstrs:
                    if fuzz.ratio(line, searchstr) > 80:
                        results.append((torrent_id, searchstr))
        page += 1
    return results