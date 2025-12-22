from typing import List, Optional

class BaseIdentifier:
    catalog: Optional[str] = None
    db: Optional[str] = None

    def is_catalog_name_equal(self, catalog_name: str) -> bool:
        """Check if the catalog name is equal, ignoring case."""
        if self.catalog and catalog_name:
            return compare_object_names(self.catalog, catalog_name)
        return True

    def is_db_name_equal(self, db_name: str) -> bool:
        """Check if the database name is equal, ignoring case."""
        if self.db and db_name:
            return compare_object_names(self.db, db_name)
        return True