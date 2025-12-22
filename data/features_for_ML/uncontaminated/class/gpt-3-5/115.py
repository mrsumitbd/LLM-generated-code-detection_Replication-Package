class Solution:
    
    def has_cycle(self, head: ListNode[int] | None) -> bool:
        if not head:
            return False
        
        slow = head
        fast = head.next
        
        while fast and fast.next:
            if slow == fast:
                return True
            slow = slow.next
            fast = fast.next.next
        
        return False