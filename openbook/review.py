"""Accuracy-review pass: count [VERIFY] and emit review prompts."""
from __future__ import annotations

import re
from pathlib import Path

from .book import Book
from .config import say
from .writer import is_done, read


def count_verify(text: str) -> int:
    return len(re.findall(r"\[VERIFY\]", text, flags=re.I))


def review_book(book: Book) -> None:
    book.review_dir.mkdir(parents=True, exist_ok=True)
    total_flags = 0
    reviewed = 0
    for path in book.section_files():
        if not is_done(path):
            continue
        text = read(path)
        n = count_verify(text)
        total_flags += n
        prompt = f"""You are a skeptical accuracy reviewer for a textbook section.

Book: {book.title}
Section: {path.name}

Mark any unsupported factual claims. Keep correct material.
Resolve or confirm each [VERIFY] if you can from reliable public knowledge;
otherwise leave [VERIFY] and note why in a short review log.

Return:
1) The corrected Markdown section
2) A short bullet list of changes / remaining concerns

Section text:
{text}
"""
        out = book.review_dir / (path.stem + ".review-prompt.txt")
        out.write_text(prompt, encoding="utf-8")
        log = book.review_dir / (path.stem + ".flags.txt")
        log.write_text(f"[VERIFY] count: {n}\n", encoding="utf-8")
        reviewed += 1
        say(f"  {path.name}: {n} [VERIFY] → {out.name}")

    say(f"Reviewed prompts for {reviewed} section(s); {total_flags} [VERIFY] flag(s) total")
    say("Paste review prompts into your AI; save corrected sections back to sections/")
