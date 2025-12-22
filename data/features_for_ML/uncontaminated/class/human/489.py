from typing import Optional, List, Set, Any

class BackwardCompatibility:
    """Helper functions for maintaining backward compatibility during migration"""

    @staticmethod
    async def dual_id_lookup(new_id: str, old_id: str, client) -> Optional[Any]:
        """
        Try to find an item by both new and old ID formats.

        Args:
            new_id: New format ID (SHA-256)
            old_id: Old format ID (MD5)
            client: Database client

        Returns:
            Found item or None
        """
        # Try new ID first
        result = await client.get(new_id)
        if result:
            return result

        # Fall back to old ID for backward compatibility
        return await client.get(old_id)

    @staticmethod
    def get_collection_name(project: str, mode: str, version: str = "v4") -> str:
        """
        Get collection name with backward compatibility.

        Args:
            project: Project name
            mode: Embedding mode (local/cloud)
            version: Collection version

        Returns:
            Collection name
        """
        if version == "v3":
            # Old format
            suffix = "_local" if mode == "local" else "_voyage"
            return f"{project}{suffix}"
        else:
            # New format with dimensions
            dim = "384d" if mode == "local" else "1024d"
            return f"csr_{project}_{mode}_{dim}"