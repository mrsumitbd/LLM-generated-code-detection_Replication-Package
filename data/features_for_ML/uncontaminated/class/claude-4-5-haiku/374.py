class Solution:

    def update_matrix(self, mat: list[list[int]]) -> list[list[int]]:
        if not mat or not mat[0]:
            return mat
        
        rows, cols = len(mat), len(mat[0])
        queue = []
        visited = [[False] * cols for _ in range(rows)]
        
        # Initialize queue with all 0s
        for i in range(rows):
            for j in range(cols):
                if mat[i][j] == 0:
                    queue.append((i, j))
                    visited[i][j] = True
        
        # BFS from all 0s
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while queue:
            row, col = queue.pop(0)
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if 0 <= new_row < rows and 0 <= new_col < cols and not visited[new_row][new_col]:
                    visited[new_row][new_col] = True
                    mat[new_row][new_col] = mat[row][col] + 1
                    queue.append((new_row, new_col))
        
        return mat