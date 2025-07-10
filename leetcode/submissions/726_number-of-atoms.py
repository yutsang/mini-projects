class Solution:
    def countOfAtoms(self, formula: str) -> str:
        def parse_formula(formula):
            stack = [defaultdict(int)]
            i = 0
            n = len(formula)
            
            while i < n:
                if formula[i] == '(':
                    stack.append(defaultdict(int))
                    i += 1
                elif formula[i] == ')':
                    i += 1
                    start = i
                    while i < n and formula[i].isdigit():
                        i += 1
                    multiplicity = int(formula[start:i] or 1)
                    top = stack.pop()
                    for elem, count in top.items():
                        stack[-1][elem] += count * multiplicity
                else:
                    start = i
                    i += 1
                    while i < n and formula[i].islower():
                        i += 1
                    elem = formula[start:i]
                    start = i
                    while i < n and formula[i].isdigit():
                        i += 1
                    multiplicity = int(formula[start:i] or 1)
                    stack[-1][elem] += multiplicity
            
            return stack[0]
        
        atom_counts = parse_formula(formula)
        sorted_atoms = sorted(atom_counts.items())
        result = []
        
        for atom, count in sorted_atoms:
            result.append(atom)
            if count > 1:
                result.append(str(count))
        
        return ''.join(result)