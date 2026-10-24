"""Progress report for a book."""
from __future__ import annotations

import re

from .book import Book
from .config import say
from .review import count_verify
from .writer import read


def status_book(book: Book) -> None:
    if not book.toml_path.is_file():
        raise SystemExit(f"No book.toml at {book.toml_path}")

    rows = book.section_status()
    done = sum(1 for _, s in rows if s == "done")
    placeholder = sum(1 for _, s in rows if s == "placeholder")
    empty = sum(1 for _, s in rows if s == "empty")
    total = len(rows)

    flags = 0
    words = 0
    for name, st in rows:
        if st != "done":
            continue
        text = read(book.sections_dir / name)
        flags += count_verify(text)
        words += len(re.findall(r"\b\w+\b", text))

    pages = max(1, words // 300) if words else 0

    say(f"Book: {book.title}  ({book.slug})")
    say(f"  sections: {done} done / {placeholder} placeholder / {empty} empty  (of {total})")
    say(f"  words (done): {words}  ~{pages} pages")
    say(f"  [VERIFY] flags: {flags}")
    say(f"  learner: {book.get('learner_name', '')}  age={book.get('learner_age', '')}")
    notes = book.get("learner_notes") or ""
    if notes:
        say(f"  notes: {notes[:120]}{'…' if len(notes) > 120 else ''}")
    for name, st in rows:
        mark = {"done": "✓", "placeholder": "·", "empty": " "}[st]
        say(f"    [{mark}] {name}")
