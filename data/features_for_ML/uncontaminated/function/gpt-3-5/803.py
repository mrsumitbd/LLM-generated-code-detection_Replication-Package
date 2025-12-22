def _fetch_database_id(notion: Client, parent_page_id: str, db_title: str) -> str | None:
    databases = notion.get_block(parent_page_id).children.filter(type="database")
    for database in databases:
        if database.title == db_title:
            return database.id
    return None