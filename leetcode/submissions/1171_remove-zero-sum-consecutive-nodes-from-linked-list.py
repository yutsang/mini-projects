# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def removeZeroSumSublists(self, head: ListNode) -> ListNode:
        dummy = ListNode(0)
        dummy.next = head
        prefix_sum = 0
        prefix_map = {0: dummy}
        
        current = head
        while current:
            prefix_sum += current.val
            if prefix_sum in prefix_map:
                node = prefix_map[prefix_sum].next
                sum_in_between = prefix_sum
                while node != current:
                    sum_in_between += node.val
                    del prefix_map[sum_in_between]
                    node = node.next
                prefix_map[prefix_sum].next = current.next
            else:
                prefix_map[prefix_sum] = current
            current = current.next
        
        return dummy.next
        