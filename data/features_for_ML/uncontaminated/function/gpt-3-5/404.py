def choose_language():
    languages = ['Python', 'Java', 'C++', 'JavaScript', 'Ruby']
    print("Choose a programming language:")
    for i, language in enumerate(languages, 1):
        print(f"{i}. {language}")
    choice = int(input("Enter the number corresponding to your choice: "))
    if choice < 1 or choice > len(languages):
        print("Invalid choice. Please try again.")
        return choose_language()
    return languages[choice - 1]