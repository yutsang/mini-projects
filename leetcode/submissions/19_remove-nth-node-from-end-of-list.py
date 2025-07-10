class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        # Create a dummy node to handle edge cases such as removing the head
        dummy = ListNode(0)
        dummy.next = head
        
        # Initialize two pointers, both starting at the dummy node
        first = dummy
        second = dummy
        
        # Move the first pointer n+1 steps ahead to maintain a gap of n between first and second
        for _ in range(n + 1):
            first = first.next
        
        # Move both pointers until the first pointer reaches the end
        while first:
            first = first.next
            second = second.next
        
        # The second pointer is now at the node before the one to be removed
        second.next = second.next.next
        
        # Return the head of the modified list
        return dummy.next

# Helper function to create a linked list from a list of values
def create_linked_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for value in values[1:]:
        current.next = ListNode(value)
        current = current.next
    return head

# Helper function to convert a linked list back to a list of values
def linked_list_to_list(head):
    values = []
    current = head
    while current:
        values.append(current.val)
        current = current.next
    return values