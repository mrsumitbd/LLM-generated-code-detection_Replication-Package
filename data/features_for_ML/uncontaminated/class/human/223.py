
class MemoryOptimizer:
    """Fix for High Issue #10: Memory Leak - Decay Processing"""

    @staticmethod
    def calculate_safe_limit(requested_limit: int, memory_factor: float = 1.5) -> int:
        """
        Calculate safe limit to prevent memory explosion.

        Args:
            requested_limit: User-requested limit
            memory_factor: Multiplication factor (reduced from 3x to 1.5x)

        Returns:
            Safe limit value
        """
        # Cap the multiplication factor to prevent OOM
        safe_factor = min(memory_factor, 2.0)

        # Also cap absolute value
        max_safe_limit = 1000

        calculated = int(requested_limit * safe_factor)
        return min(calculated, max_safe_limit)