class Solution:
    def findLongestChain(self, pairs: List[List[int]]) -> int:
        # Step 1: Sort the pairs based on the second element (right)
        pairs.sort(key=lambda x: x[1])
        
        # Step 2: Initialize the count of pairs in the chain
        chain_length = 0
        
        # Step 3: Initialize the end of the last pair in the chain
        current_end = float('-inf')

        # Step 4: Iterate through the pairs
        for left, right in pairs:
            # If the current pair can be attached to the chain
            if left > current_end:
                # Step 5: Update the end of the last pair in the chain
                current_end = right
                # Increment the chain length
                chain_length += 1

        return chain_length