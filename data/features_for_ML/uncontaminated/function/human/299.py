from loguru import logger

def get_database_tables(db: str) -> str:
    logger.debug(f"Fetching tables from database {db}")
    result = db_client.execute(f"SHOW TABLES FROM {db}")
    logger.debug(f"Found {len(result.rows) if result.success and result.rows else 0} tables in {db}")
    return result.to_string()