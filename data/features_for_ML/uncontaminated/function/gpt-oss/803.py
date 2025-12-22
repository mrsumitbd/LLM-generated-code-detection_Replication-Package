from typing import Optional
from notion_client import Client  # type: ignore

def _fetch_database_id(
    notion: Client, parent_page_id: str, db_title: str
) -> Optional[str]:
    """
    Locate a child database by title inside a given page.

    Parameters
    ----------
    notion : Client
        An authenticated Notion client.
    parent_page_id : str
        The ID of the page that may contain the child database.
    db_title : str
        The title of the child database to locate.

    Returns
    -------
    Optional[str]
        The database ID if found, otherwise None.
    """
    # Iterate over all child blocks of the page, handling pagination.
    cursor: Optional[str] = None
    while True:
        response = notion.blocks.children.list(
            block_id=parent_page_id,
            start_cursor=cursor,
            page_size=100,
        )
        for block in response.get("results", []):
            # Child database blocks have type 'child_database'.
            if block.get("type") == "child_database":
                child_db = block.get("child_database", {})
                title = child_db.get("title")
                if title == db_title:
                    return child_db.get("database_id")
        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")
    return None