import random
import requests
from bs4 import BeautifulSoup

def get_random_audiobook_covers_with_links():
    audiobook_covers = []
    audiobook_links = []

    url = "https://www.audible.com/search?keywords=audiobooks&ref=a_hp_t1_header_search"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    product_containers = soup.find_all("li", class_="productListItem")

    for container in random.sample(product_containers, 3):
        cover_img = container.find("img", class_="productImage")
        cover_link = container.find("a", class_="bc-link")

        if cover_img and cover_link:
            audiobook_covers.append(cover_img["src"])
            audiobook_links.append(cover_link["href"])

    return audiobook_covers, audiobook_links