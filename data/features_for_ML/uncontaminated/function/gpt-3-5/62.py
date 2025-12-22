def get_voltages(shotn):
    voltages = []
    for i in range(1, shotn + 1):
        voltages.append(i * 10)
    return voltages