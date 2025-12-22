class MemoryOptimizer:
    """Fix for High Issue #10: Memory Leak - Decay Processing"""

    @staticmethod
    def calculate_safe_limit(requested_limit: int, memory_factor: float = 1.5) -> int:
        """
        Calculates a safe memory limit based on the requested limit and a memory factor.

        Args:
            requested_limit (int): The requested memory limit.
            memory_factor (float, optional): The memory factor to apply. Defaults to 1.5.

        Returns:
            int: The calculated safe memory limit.
        """
        safe_limit = int(requested_limit * memory_factor)
        return safe_limit