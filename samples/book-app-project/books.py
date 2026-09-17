import json
from dataclasses import asdict, dataclass
from typing import List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    """Represent a book in the collection."""

    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    """Manage books stored in the app's JSON data file."""

    def __init__(self):
        """Create a collection and load its books from disk."""
        self.books: List[Book] = []
        self.load_books()

    @staticmethod
    def _validate_title(title: str) -> str:
        """Validate that a title is a non-empty string."""
        if not isinstance(title, str):
            raise ValueError("Book title must be a string.")

        normalized_title = title.strip()
        if not normalized_title:
            raise ValueError("Book title cannot be empty.")

        return normalized_title

    def load_books(self) -> None:
        """Load books from JSON, or start empty when the file is unavailable.

        A missing file starts a new collection. Invalid JSON is reported with a
        warning and also results in an empty collection. Other file or record
        errors are not hidden, so callers can see unexpected failures.
        """
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self) -> None:
        """Save the current collection to JSON.

        File-system errors are allowed to propagate so the CLI can present a
        clear user-facing message instead of reporting a false success.
        """
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Validate and add a book, then persist the updated collection.

        Raises:
            ValueError: If ``title`` is not a non-empty string.
        """
        normalized_title = self._validate_title(title)
        book = Book(title=normalized_title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return all books in insertion order."""
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by case-insensitive title.

        Raises:
            ValueError: If ``title`` is not a non-empty string.
        """
        normalized_title = self._validate_title(title)
        for book in self.books:
            if book.title.lower() == normalized_title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark a matching book as read and persist the collection.

        Returns:
            True when a book was found and updated, otherwise False.

        Raises:
            ValueError: If ``title`` is not a non-empty string.
        """
        normalized_title = self._validate_title(title)
        book = self.find_book_by_title(normalized_title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by exact, case-insensitive title.

        Returns:
            True if a matching book was removed, otherwise False.
        """
        normalized_title = self._validate_title(title)
        book = self.find_book_by_title(normalized_title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books whose authors match case-insensitively.

        Returns:
            A list of matching books, which may be empty.
        """
        return [b for b in self.books if b.author.lower() == author.lower()]
