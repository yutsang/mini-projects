class Solution:
    def dividePlayers(self, skill: List[int]) -> int:
        skill.sort()  # Step 1: Sort the skill levels
        n = len(skill)
        
        total_skill = sum(skill)  # Calculate total skill
        if total_skill % (n // 2) != 0:
            return -1  # If total skill cannot be evenly divided, return -1
        
        target_skill = total_skill // (n // 2)  # Target skill for each team
        total_chemistry = 0
        
        # Step 3: Form teams and calculate chemistry
        for i in range(n // 2):
            team_skill = skill[i] + skill[n - 1 - i]  # Pair the i-th and (n-1-i)-th player
            if team_skill != target_skill:
                return -1  # If the team skill does not match the target, return -1
            total_chemistry += skill[i] * skill[n - 1 - i]  # Calculate chemistry
        
        return total_chemistry