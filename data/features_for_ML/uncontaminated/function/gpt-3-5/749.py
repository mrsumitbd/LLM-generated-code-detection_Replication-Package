def audiobookshelf():
    audiobooks = []
    while True:
        action = input("Enter 'a' to add a book, 'l' to list books, or 'q' to quit: ")
        if action == 'a':
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            genre = input("Enter the genre of the book: ")
            audiobooks.append({'title': title, 'author': author, 'genre': genre})
        elif action == 'l':
            if audiobooks:
                print("Your audiobookshelf:")
                for i, book in enumerate(audiobooks, 1):
                    print(f"{i}. {book['title']} by {book['author']} - {book['genre']}")
            else:
                print("Your audiobookshelf is empty.")
        elif action == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")

audiobookshelf()