# Book Collection App

*(This README is intentionally rough so you can improve it with GitHub Copilot CLI)*

A Python app for managing books you have or want to read.
It can add, remove, and list books. Also mark them as read.

---

## Current Features

* Reads books from a JSON file (our database)
* Searches for books published within a year range
* Input checking is weak in some areas
* Some tests exist but probably not enough

---

## Files

* `book_app.py` - Main CLI entry point
* `books.py` - BookCollection class with data logic
* `utils.py` - Helper functions for UI and input
* `data.json` - Sample book data
* `tests/test_books.py` - Starter pytest tests

---

## Running the App

Start the interactive menu by default:

```bash
python -m pip install -e .
python book_app.py
```

You can also run the app with direct commands:

```bash
python book_app.py list
python book_app.py add
python book_app.py find
python book_app.py search-year
python book_app.py remove
python book_app.py menu
python book_app.py help
```

During an interactive action, type `cancel` at any prompt to return to the
main menu without saving changes.

## Running Tests

```bash
python -m pytest tests/
```

## Search by Year

Use the `search-year` command to find books published between two years:

```bash
python book_app.py search-year
```

The app prompts you for a start year and an end year. Both years are
included in the search, so entering `1950` and `1960` finds books published
from 1950 through 1960. The start year must not be later than the end year.

For example:

```text
Find Books by Publication Year

Start year: 1950
End year: 1960
```

---

## Notes

* Not production-ready (obviously)
* Some code could be improved
* Could add more commands later
