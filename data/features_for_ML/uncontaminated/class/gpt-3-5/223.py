class MemoryOptimizer:
    """Fix for High Issue #10: Memory Leak - Decay Processing"""

    @staticmethod
    def calculate_safe_limit(requested_limit: int, memory_factor: float = 1.5) -> int:
        return int(requested_limit * memory_factor)