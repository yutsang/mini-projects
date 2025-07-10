class Solution:
    @staticmethod
    def survivedRobotsHealths(positions, healths, directions):
        robots = list(zip(positions, healths, directions, range(len(positions))))
        
        robots.sort()
        
        stack = []
        
        for pos, health, direction, index in robots:
            if direction == 'R':
                stack.append((pos, health, direction, index))
            else:  # direction == 'L'
                while stack and stack[-1][2] == 'R':
                    r_pos, r_health, r_direction, r_index = stack.pop()
                    if r_health > health:
                        r_health -= 1
                        stack.append((r_pos, r_health, r_direction, r_index))
                        break
                    elif r_health < health:
                        health -= 1
                    else:
                        break
                else:
                    stack.append((pos, health, direction, index))
        
        surviving_robots = sorted(stack, key=lambda x: x[3])
        
        return [health for _, health, _, _ in surviving_robots]