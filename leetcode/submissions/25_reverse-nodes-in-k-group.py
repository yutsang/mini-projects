class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        def reverseLinkedList(head: ListNode, k: int) -> ListNode:
            new_head, ptr = None, head
            while k:
                next_node = ptr.next
                ptr.next = new_head
                new_head = ptr
                ptr = next_node
                k -= 1
            return new_head
        
        ptr = head
        count = 0
        while ptr and count < k:
            ptr = ptr.next
            count += 1
        
        if count == k:
            reversed_head = reverseLinkedList(head, k)
            head.next = self.reverseKGroup(ptr, k)
            return reversed_head
        return head

    def create_linked_list(self, values):
        if not values:
            return None
        head = ListNode(values[0])
        current = head
        for value in values[1:]:
            current.next = ListNode(value)
            current = current.next
        return head

    def linked_list_to_list(self, head):
        result = []
        while head:
            result.append(head.val)
            head = head.next
        return result