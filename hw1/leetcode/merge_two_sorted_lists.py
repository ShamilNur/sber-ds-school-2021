class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def merge_two_lists(self, l1: ListNode, l2: ListNode) -> ListNode:
        if l1 is None:
            return l2
        if l2 is None:
            return l1

        head = None
        curr = None
        a = l1
        b = l2

        while a is not None and b is not None:
            if head is None:
                if a.val <= b.val:
                    curr = a
                    head = curr
                    a = a.next
                else:
                    curr = b
                    head = curr
                    b = b.next
            else:
                if a.val <= b.val:
                    curr.next = a
                    curr = a
                    a = a.next
                else:
                    curr.next = b
                    curr = b
                    b = b.next

        if a is not None:
            curr.next = a
        if b is not None:
            curr.next = b

        return head
