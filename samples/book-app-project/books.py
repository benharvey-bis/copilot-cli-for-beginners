import json
from dataclasses import asdict, dataclass
from typing import List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self):
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

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        normalized_title = self._validate_title(title)
        book = Book(title=normalized_title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        normalized_title = self._validate_title(title)
        for book in self.books:
            if book.title.lower() == normalized_title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
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
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]
