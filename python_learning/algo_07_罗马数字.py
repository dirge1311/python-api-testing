def romanToInt(s):
    roman = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }
    total = 0
    n = len(s)
    for i in range(n):
        cur = roman[s[i]]
        if i < n - 1 and cur < roman[s[i + 1]]:
            total = total - cur
        else:
            total = total + cur
    return total
print(romanToInt("III"))     # 3
print(romanToInt("IV"))      # 4
print(romanToInt("IX"))      # 9
print(romanToInt("LVIII"))   # 58