def dupe_check_recent_torrents(gazelle_site, searchstrs):
    import requests
    from difflib import SequenceMatcher
    from bs4 import BeautifulSoup

    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def fetch_page(url):
        response = requests.get(url)
        return response.text

    def get_torrent_titles(site_url):
        page = fetch_page(site_url)
        soup = BeautifulSoup(page, 'html.parser')
        titles = [title.text for title in soup.find_all('a', class_='torrent_title')]
        return titles

    def check_for_duplicates(searchstr, titles):
        for title in titles:
            similarity = similar(searchstr, title)
            if similarity > 0.8:
                return True
        return False

    site_url = f'{gazelle_site}/log.php'
    titles = get_torrent_titles(site_url)

    for searchstr in searchstrs:
        if check_for_duplicates(searchstr, titles):
            return True

    return False