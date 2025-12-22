import requests
from bs4 import BeautifulSoup
import random

def get_random_audiobook_covers_with_links():
    url = 'https://librivox.org/search?title=&author=&reader=&keywords=&genre_id=0&status=all&project_type=solo&recorded_language=&sort_order=catalog_date&search_page=1&search_form=advanced'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    covers_with_links = []
    for item in soup.find_all('div', class_='catalog-result'):
        cover = item.find('img')['src']
        link = item.find('a')['href']
        covers_with_links.append((cover, link))
    random_cover_with_link = random.choice(covers_with_links)
    return random_cover_with_link