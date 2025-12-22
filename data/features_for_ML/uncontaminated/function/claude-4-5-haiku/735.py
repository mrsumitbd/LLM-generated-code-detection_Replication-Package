def __compress(result, target: str, power: int):
    if power == 0:
        result.append(target)
    else:
        half_power = power // 2
        __compress(result, target, half_power)
        __compress(result, target + target, half_power)