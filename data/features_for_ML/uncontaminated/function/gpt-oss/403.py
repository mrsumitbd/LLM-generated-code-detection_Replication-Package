import random
from typing import List, Tuple

def get_random_audiobook_covers_with_links() -> List[Tuple[str, str]]:
    """
    Return a random selection of audiobook cover URLs paired with their corresponding
    audiobook page URLs. The function uses a small static dataset of popular
    audiobooks. Each call returns a random subset of the dataset.

    Returns:
        List[Tuple[str, str]]: A list where each element is a tuple
        (cover_url, audiobook_page_url).
    """
    # Static dataset of (cover_url, audiobook_page_url) pairs
    dataset = [
        (
            "https://covers.openlibrary.org/b/id/8231856-L.jpg",
            "https://openlibrary.org/works/OL82563W/To_Kill_a_Mockingbird",
        ),
        (
            "https://covers.openlibrary.org/b/id/8231857-L.jpg",
            "https://openlibrary.org/works/OL82564W/The_Great_Gatsby",
        ),
        (
            "https://covers.openlibrary.org/b/id/8231858-L.jpg",
            "https://openlibrary.org/works/OL82565W/1984",
        ),
        (
            "https://covers.openlibrary.org/b/id/8231859-L.jpg",
            "https://openlibrary.org/works/OL82566W/Brave_New_World",
        ),
        (
            "https://covers.openlibrary.org/b/id/8231860-L.jpg",
            "https://openlibrary.org/works/OL82567W/Animal_Farm",
        ),
        (
            "https://covers.openlibrary.org/b/id/8231861-L.jpg",
            "https://openlibrary.org/works/OL82568W/War_and_Peace",
        ),
        (
            "https://covers.openlibrary.org/b/id/8231862-L.jpg",
            "https://openlibrary.org/works/OL82569W/Pride_and_Prejudice",
        ),
        (
            "https://covers.openlibrary.org/b/id/8231863-L.jpg",
            "https://openlibrary.org/works/OL82570W/Moby_Dick",
        ),
        (
            "https://covers.openlibrary.org/b/id/8231864-L.jpg",
            "https://openlibrary.org/works/OL82571W/Great_Expectations",
        ),
        (
            "https://covers.openlibrary.org/b/id/8231865-L.jpg",
            "https://openlibrary.org/works/OL82572W/Crime_and_Punishment",
        ),
    ]

    # Decide how many items to return (between 1 and the size of the dataset)
    num_items = random.randint(1, len(dataset))

    # Randomly sample without replacement
    selected = random.sample(dataset, num_items)

    return selected