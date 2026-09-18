import sys
from collections.abc import Callable, Sequence

try:
    from prompt_toolkit import prompt as interactive_prompt
    from prompt_toolkit.completion import WordCompleter
except ImportError:  # pragma: no cover - platform-specific fallback
    interactive_prompt = None
    WordCompleter = None

from books import Book, BookCollection

# Global collection instance
collection = BookCollection()
CANCEL_COMMAND = "cancel"


class ActionCancelled(Exception):
    """Signal that the user wants to return to the main menu."""


def get_title_options() -> list[str]:
    return sorted({book.title for book in collection.books})


def get_author_options() -> list[str]:
    return sorted({book.author for book in collection.books})


def prompt_for_value(prompt: str, options: Sequence[str]) -> str:
    """Prompt the user and allow tab completion for known values."""
    if interactive_prompt is not None and WordCompleter is not None:
        completer = WordCompleter(
            list(options),
            ignore_case=True,
            sentence=True,
        )
        value = interactive_prompt(prompt, completer=completer)
    else:
        value = input(prompt)

    if value.strip().lower() == CANCEL_COMMAND:
        raise ActionCancelled
    return value


def prompt_for_input(prompt: str) -> str:
    """Prompt without completion and allow the user to cancel the action."""
    value = input(prompt)
    if value.strip().lower() == CANCEL_COMMAND:
        raise ActionCancelled
    return value


def show_books(books: Sequence[Book]) -> None:
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print()


def handle_list() -> None:
    books = collection.list_books()
    show_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    try:
        title = prompt_for_value("Title: ", get_title_options()).strip()
        author = prompt_for_value("Author: ", get_author_options()).strip()
        year_str = prompt_for_input("Year: ").strip()

        if not title:
            raise ValueError("Book title cannot be empty.")

        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ActionCancelled:
        print("\nAdd cancelled. Returning to the main menu.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_mark_as_read() -> None:
    print("\nMark a Book as Read\n")

    try:
        title = prompt_for_value(
            "Enter the title of the book: ", get_title_options()
        ).strip()
        if not title:
            raise ValueError("Book title cannot be empty.")

        if collection.mark_as_read(title):
            print("\nBook marked as read.\n")
        else:
            print("\nBook not found.\n")
    except ActionCancelled:
        print("\nMark-as-read cancelled. Returning to the main menu.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove() -> None:
    print("\nRemove a Book\n")

    try:
        title = prompt_for_value(
            "Enter the title of the book to remove: ", get_title_options()
        ).strip()
        if not title:
            raise ValueError("Book title cannot be empty.")

        if collection.remove_book(title):
            print("\nBook removed successfully.\n")
        else:
            print("\nBook not found.\n")
    except ActionCancelled:
        print("\nRemove cancelled. Returning to the main menu.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_find() -> None:
    print("\nFind Books by Author\n")

    try:
        author = prompt_for_value("Author name: ", get_author_options()).strip()
        books = collection.find_by_author(author)
        show_books(books)
    except ActionCancelled:
        print("\nAuthor search cancelled. Returning to the main menu.\n")


def handle_search_year() -> None:
    print("\nFind Books by Publication Year\n")

    try:
        start_year_str = prompt_for_input("Start year: ").strip()
        end_year_str = prompt_for_input("End year: ").strip()
        start_year = int(start_year_str)
        end_year = int(end_year_str)
        books = collection.find_by_year_range(start_year, end_year)
    except ActionCancelled:
        print("\nYear search cancelled. Returning to the main menu.\n")
        return
    except ValueError as e:
        print(f"\nError: {e}\n")
        return

    show_books(books)


def show_menu() -> None:
    print("\nBook Collection Menu")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Find books by author")
    print("6. Search books by year range")
    print("7. Exit")
    print("(Type 'cancel' at any action prompt to return here.)")


def run_interactive_menu() -> None:
    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            handle_add()
        elif choice == "2":
            handle_list()
        elif choice == "3":
            handle_mark_as_read()
        elif choice == "4":
            handle_remove()
        elif choice == "5":
            handle_find()
        elif choice == "6":
            handle_search_year()
        elif choice == "7":
            print("\nGoodbye!\n")
            return
        else:
            print("\nInvalid choice. Please select a number from 1 to 7.\n")


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  search-year - Find books published between two years
  menu     - Start the interactive menu
  help     - Show this help message
""")


CommandHandler = Callable[[], None]

COMMAND_HANDLERS: dict[str, CommandHandler] = {
    "list": handle_list,
    "add": handle_add,
    "remove": handle_remove,
    "find": handle_find,
    "search-year": handle_search_year,
    "menu": run_interactive_menu,
    "interactive": run_interactive_menu,
    "help": show_help,
}


def main() -> None:
    if len(sys.argv) < 2:
        run_interactive_menu()
        return

    command = sys.argv[1].lower()

    handler = COMMAND_HANDLERS.get(command)
    if handler is None:
        print("Unknown command.\n")
        show_help()
        return

    handler()


if __name__ == "__main__":
    main()
