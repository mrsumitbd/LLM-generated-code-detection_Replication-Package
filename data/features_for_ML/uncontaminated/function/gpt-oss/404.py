def choose_language():
    """
    Prompt the user to choose a programming language from a predefined list.
    Returns the chosen language as a string.
    """
    options = {
        "1": "Python",
        "2": "JavaScript",
        "3": "C++",
        "4": "Java",
        "5": "Other"
    }

    prompt_lines = ["Choose a programming language:"]
    for key, value in options.items():
        prompt_lines.append(f"  {key}. {value}")
    prompt_lines.append("Enter the number of your choice: ")

    while True:
        choice = input("\n".join(prompt_lines)).strip()
        if choice in options:
            return options[choice]
        print("Invalid choice. Please try again.\n")