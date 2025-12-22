def system_prompt(natural=False, sab=False, **kwargs):
    if natural:
        print("Natural system prompt")
    elif sab:
        print("Sab system prompt")
    else:
        print("Default system prompt")
    
    for key, value in kwargs.items():
        print(f"{key}: {value}")