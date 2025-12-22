class SolutionMath:

    def unique_paths(self, m: int, n: int) -> int:
        """
        Calculate the number of unique paths in an m x n grid.
        You can only move right or down.
        
        Args:
            m: number of rows
            n: number of columns
            
        Returns:
            number of unique paths from top-left to bottom-right
        """
        # Create a 2D DP table
        dp = [[1] * n for _ in range(m)]
        
        # Fill the DP table
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
        
        return dp[m-1][n-1]