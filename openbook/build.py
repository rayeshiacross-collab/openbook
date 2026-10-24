"""Assemble Markdown textbook + solutions stub; optional PDF if tools exist."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from .book import Book
from .config import say
from .writer import is_done, read


def assemble(book: Book, *, include_unfinished: bool = False):
    parts = [f"# {book.title}\n"]
    if book.get("subtitle"):
        parts.append(f"*{book.get('subtitle')}*\n")
    parts.append(f"\nSubject: {book.get('subject', '')}\n")
    parts.append(
        f"Learner profile: {book.get('learner_name', '')} "
        f"(age {book.get('learner_age', '')})\n"
    )
    if book.get("learner_notes"):
        parts.append(f"Notes: {book.get('learner_notes')}\n")
    parts.append("\n---\n\n")

    solutions = [f"# Solutions — {book.title}\n\n"]
    missing = []
    for path in book.section_files():
        if not is_done(path):
            missing.append(path.name)
            if not include_unfinished:
                continue
        text = read(path).strip()
        parts.append(text + "\n\n")
        if re.search(r"problem|exercise|solution", path.name, re.I):
            solutions.append(f"## {path.stem}\n\n_(Add worked solutions.)_\n\n")

    return "\n".join(parts), "\n".join(solutions), missing


def build_book(book: Book, *, dyslexia: bool = False, visual: bool = False) -> Path:
    book.out_dir.mkdir(parents=True, exist_ok=True)
    text, sols, missing = assemble(book)
    if not text.strip() or text.count("\n") < 5:
        raise SystemExit("Nothing to build yet: finish at least one section.")

    md_path = book.out_dir / f"{book.slug}.md"
    sol_path = book.out_dir / f"{book.slug}-solutions.md"
    md_path.write_text(text, encoding="utf-8")
    sol_path.write_text(sols, encoding="utf-8")
    say(f"Wrote {md_path}")
    say(f"Wrote {sol_path}")
    if missing:
        say(f"Skipped {len(missing)} unfinished section(s)")

    pdf = book.out_dir / f"{book.slug}.pdf"
    if shutil.which("pandoc"):
        cmd = ["pandoc", str(md_path), "-o", str(pdf), "--from", "markdown"]
        if dyslexia or book.get("dyslexia_support"):
            say("Dyslexia layout: prefer OpenDyslexic in your PDF engine if available")
        if visual or book.get("visual_support"):
            say("Visual layout: larger type / wider margins recommended")
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if r.returncode == 0 and pdf.is_file():
                say(f"Wrote {pdf}")
            else:
                say(f"PDF skipped: {(r.stderr or 'pandoc failed')[:200]}")
        except Exception as e:
            say(f"PDF skipped: {e}")
    else:
        say("PDF skipped (install pandoc for Markdown→PDF)")

    return md_path
