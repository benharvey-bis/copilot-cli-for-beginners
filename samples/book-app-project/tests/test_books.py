import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False


def test_add_book_with_empty_title_raises_value_error():
    collection = BookCollection()

    with pytest.raises(ValueError, match="Book title cannot be empty"):
        collection.add_book("   ", "George Orwell", 1949)


def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None


def test_remove_book_matches_title_case_insensitively():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    result = collection.remove_book("tHe HoBbIt")

    assert result is True
    assert collection.books == []


def test_remove_book_does_not_remove_partial_title_match():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Dune Messiah", "Frank Herbert", 1969)

    result = collection.remove_book("Dune Mes")

    assert result is False
    assert [book.title for book in collection.books] == ["Dune", "Dune Messiah"]


def test_remove_book_returns_false_when_book_does_not_exist():
    collection = BookCollection()

    result = collection.remove_book("Nonexistent Book")

    assert result is False


def test_remove_book_returns_false_for_empty_collection():
    collection = BookCollection()

    result = collection.remove_book("Dune")

    assert result is False


def test_find_by_year_range_includes_boundary_years():
    collection = BookCollection()
    collection.add_book("Old", "Author", 1949)
    collection.add_book("Middle", "Author", 1950)
    collection.add_book("New", "Author", 1951)

    result = collection.find_by_year_range(1949, 1950)

    assert [book.title for book in result] == ["Old", "Middle"]


def test_find_by_year_range_excludes_books_outside_range():
    collection = BookCollection()
    collection.add_book("Old", "Author", 1948)
    collection.add_book("New", "Author", 1951)

    result = collection.find_by_year_range(1949, 1950)

    assert result == []


def test_find_by_year_range_rejects_reversed_range():
    collection = BookCollection()

    with pytest.raises(
        ValueError, match="Start year must be less than or equal to end year"
    ):
        collection.find_by_year_range(1950, 1949)


def test_find_by_year_range_rejects_non_integer_years():
    collection = BookCollection()

    with pytest.raises(ValueError, match="Years must be integers"):
        collection.find_by_year_range("1949", 1950)


def test_find_by_year_range_rejects_boolean_years():
    collection = BookCollection()

    with pytest.raises(ValueError, match="Years must be integers"):
        collection.find_by_year_range(True, 1950)
