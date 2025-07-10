class Solution:
    def intToRoman(self, num: int) -> str:
        # Define the Roman numeral symbols and their corresponding values
        values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        
        roman = ""
        
        # Iterate through the values and symbols
        for i, value in enumerate(values):
            # While the number is greater than or equal to the current value
            while num >= value:
                # Add the corresponding symbol to the roman numeral string
                roman += symbols[i]
                # Subtract the value from the number
                num -= value
        
        return roman
        