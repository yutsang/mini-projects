class RandomizedSet:

    def __init__(self):
        self.data = []
        self.index_map = {}

    def insert(self, val: int) -> bool:
        if val in self.index_map:
            return False
        self.index_map[val] = len(self.data)
        self.data.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.index_map:
            return False
        last_element = self.data[-1]
        idx_to_remove = self.index_map[val]
        self.data[idx_to_remove] = last_element
        self.index_map[last_element] = idx_to_remove
        self.data.pop()
        del self.index_map[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.data)