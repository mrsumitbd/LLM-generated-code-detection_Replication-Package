def choose_language():
    languages = ["English", "Spanish", "French", "German", "Mandarin"]
    print("Available languages:")
    for language in languages:
        print(f"- {language}")
    
    while True:
        user_input = input("Please choose a language (or 'exit' to quit): ").strip().lower()
        if user_input == "exit":
            print("Exiting...")
            return None
        elif user_input in [lang.lower() for lang in languages]:
            return user_input.capitalize()
        else:
            print("Invalid language choice. Please try again.")