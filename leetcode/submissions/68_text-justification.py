class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        result = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + len(current_line) <= maxWidth:
                current_line.append(word)
                current_length += len(word)
            else:
                spaces_to_add = maxWidth - current_length
                if len(current_line) == 1:
                    result.append(current_line[0] + ' ' * spaces_to_add)
                else:
                    spaces_between_words = spaces_to_add // (len(current_line) - 1)
                    extra_spaces = spaces_to_add % (len(current_line) - 1)
                    line = ''
                    for i, w in enumerate(current_line[:-1]):
                        line += w + ' ' * (spaces_between_words + (1 if i < extra_spaces else 0))
                    line += current_line[-1]
                    result.append(line)
                
                current_line = [word]
                current_length = len(word)

        last_line = ' '.join(current_line)
        spaces_to_add = maxWidth - len(last_line)
        result.append(last_line + ' ' * spaces_to_add)

        return result