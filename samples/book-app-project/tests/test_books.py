import builtins
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
import book_app
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


def test_list_books_returns_books_in_insertion_order():
    collection = BookCollection()
    collection.add_book("B", "Author B", 2001)
    collection.add_book("A", "Author A", 2002)

    result = collection.list_books()

    assert [book.title for book in result] == ["B", "A"]


def test_find_by_author_matches_case_insensitively():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Foundation", "Isaac Asimov", 1951)
    collection.add_book("Dune Messiah", "Frank Herbert", 1969)

    result = collection.find_by_author("frank herbert")

    assert [book.title for book in result] == ["Dune", "Dune Messiah"]


def test_load_books_handles_missing_data_file(tmp_path, monkeypatch):
    missing_file = tmp_path / "missing_data.json"
    monkeypatch.setattr(books, "DATA_FILE", str(missing_file))

    collection = BookCollection()

    assert collection.books == []


def test_load_books_handles_invalid_json():
    collection = BookCollection()
    with open(books.DATA_FILE, "w", encoding="utf-8") as file:
        file.write("{not valid json")

    collection.load_books()

    assert collection.books == []


def test_save_books_writes_expected_json():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)

    with open(books.DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data == [{
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "read": False,
    }]


def test_validate_title_rejects_non_string_input():
    with pytest.raises(ValueError, match="Book title must be a string"):
        books.BookCollection._validate_title(123)


def test_validate_title_rejects_empty_string_after_stripping():
    with pytest.raises(ValueError, match="Book title cannot be empty"):
        books.BookCollection._validate_title("   ")


def test_find_book_by_title_rejects_empty_title():
    collection = BookCollection()

    with pytest.raises(ValueError, match="Book title cannot be empty"):
        collection.find_book_by_title("   ")


def test_mark_as_read_rejects_empty_title():
    collection = BookCollection()

    with pytest.raises(ValueError, match="Book title cannot be empty"):
        collection.mark_as_read("   ")


def test_remove_book_rejects_empty_title():
    collection = BookCollection()

    with pytest.raises(ValueError, match="Book title cannot be empty"):
        collection.remove_book("   ")


def test_find_by_year_range_rejects_float_years():
    collection = BookCollection()

    with pytest.raises(ValueError, match="Years must be integers"):
        collection.find_by_year_range(1949.0, 1950)


def test_find_by_author_matches_surname_only():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Mysterious Book", "", 0)

    result = collection.find_by_author("Orwell")

    assert [book.title for book in result] == ["1984"]


def test_book_app_completion_helpers_include_existing_values(monkeypatch):
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Dune", "Frank Herbert", 1965)
    monkeypatch.setattr(book_app, "collection", collection)

    assert book_app.get_title_options() == ["1984", "Dune"]
    assert "George Orwell" in book_app.get_author_options()


def test_main_starts_interactive_menu_when_no_arguments(monkeypatch):
    calls = []
    monkeypatch.setattr(book_app, "run_interactive_menu", lambda: calls.append("menu"))
    monkeypatch.setattr(sys, "argv", ["book_app.py"])

    book_app.main()

    assert calls == ["menu"]


def test_run_interactive_menu_exits_on_choice_seven(monkeypatch, capsys):
    inputs = iter(["7"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))
    monkeypatch.setattr(book_app, "collection", BookCollection())

    book_app.run_interactive_menu()

    captured = capsys.readouterr().out
    assert "Book Collection Menu" in captured
    assert "Goodbye!" in captured


def test_run_interactive_menu_uses_plain_menu_input(monkeypatch):
    calls = []
    monkeypatch.setattr(builtins, "input", lambda prompt="": calls.append(prompt) or "7")
    monkeypatch.setattr(book_app, "collection", BookCollection())

    book_app.run_interactive_menu()

    assert calls == ["Choose an option (1-7): "]


def test_add_book_can_be_cancelled_without_saving(monkeypatch, capsys):
    collection = BookCollection()
    monkeypatch.setattr(book_app, "collection", collection)
    monkeypatch.setattr(
        book_app,
        "prompt_for_value",
        lambda prompt, options: (_ for _ in ()).throw(book_app.ActionCancelled),
    )

    book_app.handle_add()

    assert collection.books == []
    assert "Add cancelled" in capsys.readouterr().out


def test_year_search_can_be_cancelled_at_second_prompt(monkeypatch, capsys):
    inputs = iter(["1940", "cancel"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    book_app.handle_search_year()

    assert "Year search cancelled" in capsys.readouterr().out
