from typing import List

class Solution:
    
    def count_bits(self, n: int) -> List[int]:
        result = []
        for i in range(n+1):
            result.append(bin(i).count('1'))
        return result