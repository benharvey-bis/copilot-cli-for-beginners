---
name: book-summary
description: Summarize the book collection in a clean markdown table with title, author, year, and read status; use when creating a reading list, status report, or quick overview of what is in the collection
---

# Book Summary Skill

Generate a concise markdown summary of the book collection.

## Output requirements

- Start with a heading: `# Book Collection Summary`
- Use a markdown table
- Include these columns in this exact order: `Title`, `Author`, `Year`, `Read`
- Sort books by `Year` in ascending order (oldest first)
- Use `✅` for books that have been read and `❌` for books not yet read
- Keep the output clean and easy to scan
- Use plain text values; do not add extra commentary before or after the table unless the user asks for it

## Table format

```markdown
# Book Collection Summary

| Title | Author | Year | Read |
|---|---|---:|---|
| Example Book | Example Author | 2021 | ✅ |
| Another Book | Another Author | 2023 | ❌ |
```

## Rules

1. If the read status is unknown, default to `❌`.
2. If a book is missing an author or year, keep the cell as plain text or `Unknown` rather than leaving it blank.
3. Preserve the original book title and author names exactly as provided.
4. If there are no books, respond with:

```markdown
# Book Collection Summary

No books found.
```

## Example result

```markdown
# Book Collection Summary

| Title | Author | Year | Read |
|---|---|---:|---|
| The Hobbit | J.R.R. Tolkien | 1937 | ✅ |
| The Left Hand of Darkness | Ursula K. Le Guin | 1969 | ❌ |
| Piranesi | Susanna Clarke | 2020 | ✅ |
```
