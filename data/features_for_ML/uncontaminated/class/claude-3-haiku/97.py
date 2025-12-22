class Solution:
    def is_palindrome(self, s: str) -> bool:
        # Remove non-alphanumeric characters and convert to lowercase
        s = ''.join(c.lower() for c in s if c.isalnum())

        # Compare characters from the start and end of the string
        left, right = 0, len(s) - 1
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1

        return True