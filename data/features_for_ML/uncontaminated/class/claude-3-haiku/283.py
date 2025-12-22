class BaseIdentifier:
    def __init__(self, catalog_name: str, db_name: str):
        self.catalog_name = catalog_name
        self.db_name = db_name

    def is_catalog_name_equal(self, catalog_name: str) -> bool:
        return self.catalog_name.lower() == catalog_name.lower()

    def is_db_name_equal(self, db_name: str) -> bool:
        return self.db_name.lower() == db_name.lower()