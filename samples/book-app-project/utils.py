from collections.abc import Sequence

from books import Book


def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()

        if not choice:
            print("Please enter a number from 1 to 5.")
            continue

        if not choice.isdigit():
            print("Invalid choice. Please enter a number from 1 to 5.")
            continue

        if int(choice) not in range(1, 6):
            print("Invalid choice. Please enter a number from 1 to 5.")
            continue

        return choice


def get_book_details() -> tuple[str, str, int]:
    """Prompt the user for the details of a new book.

    The title is required and the user is prompted again when it is empty.
    The author may be empty. If the publication year is empty or not a valid
    integer, it defaults to ``0`` after displaying a warning.

    Returns:
        A tuple containing the book title, author, and publication year.
        The tuple has the type ``tuple[str, str, int]``.
    """
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print("Book title cannot be empty. Please try again.")

    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books: Sequence[Book]) -> None:
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
