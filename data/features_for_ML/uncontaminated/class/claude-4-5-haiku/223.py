class MemoryOptimizer:
    """Fix for High Issue #10: Memory Leak - Decay Processing"""

    @staticmethod
    def calculate_safe_limit(requested_limit: int, memory_factor: float = 1.5) -> int:
        """
        Calculate a safe memory limit based on requested limit and memory factor.
        
        Args:
            requested_limit: The requested memory limit in bytes
            memory_factor: The factor to apply for safety margin (default 1.5)
        
        Returns:
            The safe memory limit as an integer
        """
        if requested_limit <= 0:
            return 0
        
        safe_limit = int(requested_limit / memory_factor)
        return max(safe_limit, 1)