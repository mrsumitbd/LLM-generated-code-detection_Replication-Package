def _fetch_database_id(
    notion: Client, parent_page_id: str, db_title: str
) -> str | None:
    """Locate a child database by title inside a given page."""
    try:
        page = notion.get_page(parent_page_id)
        databases = page.get("child_database", [])
        for database in databases:
            if database.title == db_title:
                return database.id
    except Exception:
        return None