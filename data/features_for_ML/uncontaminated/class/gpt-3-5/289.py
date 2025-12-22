class TableInfo:
    
    def __post_init__(self):
        self.size = 0

    @staticmethod
    def parse_size_string(size_str: str) -> int:
        return int(size_str)

    def is_large_table(self) -> bool:
        return self.size > 100

    def priority_score(self) -> float:
        return self.size * 0.5

    def is_expired(self, expire_seconds: int = 120) -> bool:
        return expire_seconds > 100