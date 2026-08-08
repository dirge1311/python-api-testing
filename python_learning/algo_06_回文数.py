def isPalindrome(x):
    s = str(x)
    return s == s[::-1]
print(isPalindrome(121))   # True
print(isPalindrome(123))   # False
print(isPalindrome(-121))  # False
print(isPalindrome(0))     # True