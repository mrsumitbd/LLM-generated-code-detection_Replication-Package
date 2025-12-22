class TableInfo:
    def __init__(self, table_name: str, table_size: str, last_accessed_time: float):
        self.table_name = table_name
        self.table_size = table_size
        self.last_accessed_time = last_accessed_time

    def __post_init__(self):
        self.table_size_bytes = self.parse_size_string(self.table_size)

    @staticmethod
    def parse_size_string(size_str: str) -> int:
        size_units = {"B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3}
        size, unit = float(size_str[:-2]), size_str[-2:]
        return int(size * size_units[unit])

    def is_large_table(self) -> bool:
        return self.table_size_bytes > 1024 ** 3  # 1 GB

    def priority_score(self) -> float:
        return self.table_size_bytes / self.last_accessed_time

    def is_expired(self, expire_seconds: int = 120) -> bool:
        from time import time
        return time() - self.last_accessed_time > expire_seconds