def diamond_peptidase_options(func):
    def wrapper(*args, **kwargs):
        print("Diamond Peptidase Options:")
        func(*args, **kwargs)
        print("Option 1: Enzyme Inhibition")
        print("Option 2: Substrate Specificity")
        print("Option 3: Structural Analysis")
    return wrapper