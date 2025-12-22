def helper(sub):
    if not sub:
        return 0
    
    max_val = 0
    for i in range(len(sub)):
        current = sub[i]
        left_sum = sum(sub[:i])
        right_sum = sum(sub[i+1:])
        
        if left_sum == right_sum:
            max_val = max(max_val, current)
    
    return max_val