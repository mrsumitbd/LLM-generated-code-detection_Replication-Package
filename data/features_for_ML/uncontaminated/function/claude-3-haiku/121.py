def display_as_textured(ref):
    try:
        if isinstance(ref, str):
            print(f"Displaying '{ref}' as textured.")
        elif isinstance(ref, list):
            for item in ref:
                if isinstance(item, str):
                    print(f"Displaying '{item}' as textured.")
                else:
                    print(f"Skipping non-string item: {item}")
        else:
            print(f"Unsupported input type: {type(ref)}")
    except Exception as e:
        print(f"Error occurred: {e}")