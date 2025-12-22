class MemoryOptimizer:
    """Fix for High Issue #10: Memory Leak - Decay Processing"""

    @staticmethod
    def calculate_safe_limit(requested_limit: int, memory_factor: float = 1.5) -> int:
        """
        Calculate a safe memory limit based on the requested limit and a decay factor.

        The safe limit is computed by dividing the requested limit by the memory_factor.
        This reduces the effective limit to mitigate memory leaks. The result is
        always at least 1.

        Parameters
        ----------
        requested_limit : int
            The original memory limit requested by the caller.
        memory_factor : float, optional
            The factor by which to reduce the requested limit. Must be > 0.
            Default is 1.5, which reduces the limit by ~33%.

        Returns
        -------
        int
            The calculated safe memory limit.

        Raises
        ------
        ValueError
            If `memory_factor` is not positive.
        """
        if memory_factor <= 0:
            raise ValueError("memory_factor must be a positive number")

        # Ensure requested_limit is non-negative
        if requested_limit < 0:
            requested_limit = 0

        safe_limit = int(requested_limit / memory_factor)
        return max(1, safe_limit)