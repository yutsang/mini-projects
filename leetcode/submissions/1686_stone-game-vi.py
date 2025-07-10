class Solution:
    def stoneGameVI(self, aliceValues: List[int], bobValues: List[int]) -> int:
        combined = [(aliceValues[i] + bobValues[i], aliceValues[i], bobValues[i]) for i in range(len(aliceValues))]
        combined.sort(reverse=True, key=lambda x: x[0])  

        alice_score = 0
        bob_score = 0

        for turn in range(len(combined)):
            if turn % 2 == 0:  
                alice_score += combined[turn][1]  
            else: 
                bob_score += combined[turn][2]  

        if alice_score > bob_score:
            return 1
        elif bob_score > alice_score:
            return -1
        else:
            return 0