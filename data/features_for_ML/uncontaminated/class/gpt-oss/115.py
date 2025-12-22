class Solution:
    def has_cycle(self, head: ListNode[int] | None) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False