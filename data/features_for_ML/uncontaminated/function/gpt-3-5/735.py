def __compress(result, target: str, power: int):
    count = 1
    for i in range(1, len(target)):
        if target[i] == target[i-1]:
            count += 1
        else:
            result += target[i-1] + str(count) if count >= power else target[i-1]*count
            count = 1
    result += target[-1] + str(count) if count >= power else target[-1]*count
    return result