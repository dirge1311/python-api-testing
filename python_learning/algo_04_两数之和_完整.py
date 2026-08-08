nums = [2, 7, 11, 15]
target = 9
for i in range(4):
    for j in range(i + 1, 4):
        sum_val = nums[i] + nums[j]
        print(f"nums[i] + nums[j] = {nums[i]} + {nums[j]} = {sum_val}")
        if sum_val == target:
            print(f"下标是[{i},{j}]")