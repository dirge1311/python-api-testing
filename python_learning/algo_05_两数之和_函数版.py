def two_Sum(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range( i+ 1, n ):
            if nums[i] + nums[j] == target:
                return [i,j]
print(two_Sum([2, 7, 11, 15], 9))
print(two_Sum([3, 2, 4], 6))
print(two_Sum([3, 3], 6))