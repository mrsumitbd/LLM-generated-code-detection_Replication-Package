def audiobookshelf():
    audiobooks = []
    while True:
        user_input = input("Enter an audiobook title (or 'q' to quit): ")
        if user_input.lower() == 'q':
            break
        audiobooks.append(user_input)
    print("Your audiobook shelf contains:")
    for book in audiobooks:
        print("- " + book)