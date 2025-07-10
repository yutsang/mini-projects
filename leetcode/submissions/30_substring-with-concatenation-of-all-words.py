class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []
        
        word_length = len(words[0])
        word_count = len(words)
        total_length = word_length * word_count
        word_map = Counter(words)
        result = []
        
        for i in range(word_length):
            left = i
            right = i
            current_count = 0
            current_map = Counter()
            
            while right + word_length <= len(s):
                word = s[right:right + word_length]
                right += word_length
                
                if word in word_map:
                    current_map[word] += 1
                    current_count += 1
                    
                    while current_map[word] > word_map[word]:
                        left_word = s[left:left + word_length]
                        current_map[left_word] -= 1
                        current_count -= 1
                        left += word_length
                    
                    if current_count == word_count:
                        result.append(left)
                else:
                    current_map.clear()
                    current_count = 0
                    left = right
        
        return result