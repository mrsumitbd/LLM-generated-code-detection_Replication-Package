def find_and_replace_pattern_with_aow_and_update_counters():
    pattern = "aow"
    counters = {"a": 0, "o": 0, "w": 0}
    
    with open("input.txt", "r") as file:
        data = file.read()
    
    data = data.replace("a", "aow").replace("o", "aow").replace("w", "aow")
    
    for char in data:
        if char in counters:
            counters[char] += 1
    
    with open("output.txt", "w") as file:
        file.write(data)
    
    return counters