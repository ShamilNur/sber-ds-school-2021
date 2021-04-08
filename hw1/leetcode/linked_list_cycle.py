class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def has_cycle(self, head: ListNode) -> bool:
        a = head
        b = head

        while b is not None and b.next is not None:
            a = a.next
            b = b.next.next
            if a == b:
                return True

        return False
