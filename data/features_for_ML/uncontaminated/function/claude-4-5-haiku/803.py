def _fetch_database_id(
    notion: Client, parent_page_id: str, db_title: str
) -> str | None:
    """Locate a child database by title inside a given page."""
    try:
        response = notion.blocks.children.list(parent_page_id)
        for block in response.get("results", []):
            if block.get("type") == "child_database":
                if block.get("child_database", {}).get("title") == db_title:
                    return block.get("id")
        return None
    except Exception:
        return None