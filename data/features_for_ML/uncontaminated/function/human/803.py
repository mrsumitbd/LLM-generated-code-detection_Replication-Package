from notion_client import Client
from tasks.utils import notion_utils

def _fetch_database_id(
    notion: Client, parent_page_id: str, db_title: str
) -> str | None:
    """Locate a child database by title inside a given page."""
    return notion_utils.find_database_in_block(notion, parent_page_id, db_title)