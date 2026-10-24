"""Create a new book directory from template."""
from __future__ import annotations

from pathlib import Path

from .book import Book, PLACEHOLDER, _slugify
from .config import ROOT, TEMPLATES_DIR, say

DEFAULT_TOML = '''# Settings for this one book. Edit freely.

title = "{title}"
subtitle = ""
subject = "{subject}"
author = ""
level = "university"
target_chapters = 12
words_per_section = 1200
language = "en-US"

learner_name = "{learner}"
learner_age = "{age}"
learner_notes = ""
reading_level = ""
reading_style = "plain"
primary_language = "en"
secondary_languages = []
glossary_every_chapter = true

attention_style = "standard"
section_max_words = 1200
checkpoint_every_n_paragraphs = 0

dyslexia_support = false
visual_support = false
auditory_support = false
hearing_support = false
adhd_support = false
autism_support = false
motor_support = false
cognitive_support = false
phonics_support = false

preferred_modalities = ["text"]
hands_on_every_chapter = false

notes = ""
voice = "Clear, respectful, precise; never condescending."
'''

DEFAULT_OUTLINE = """# Outline

Edit this table of contents, then run `python -m openbook write {slug}`.

## Chapter 1 — Introduction
- 01-01-welcome.md — What this book is and how to use it
- 01-02-how-to-read.md — How to work through the material

## Chapter 2 — Core ideas
- 02-01-first-idea.md — First major idea
- 02-02-second-idea.md — Second major idea

## Chapter 3 — Practice
- 03-01-worked-examples.md — Worked examples
- 03-02-problems.md — Graded problems
"""

DEFAULT_SOURCES = """# Sources

List openly licensed or original sources the AI should prefer.

- (add OpenStax, LibreTexts, official docs, etc.)
"""


def create(
    slug: str,
    *,
    title: str = "",
    subject: str = "",
    learner: str = "",
    age: str = "",
) -> Book:
    slug = _slugify(slug)
    book = Book(slug)
    if book.toml_path.is_file():
        raise SystemExit(f"Book already exists: {book.dir}")

    book.ensure_dirs()
    title = title or slug.replace("-", " ").title()
    subject = subject or title
    learner = learner or "the learner"
    age = age or ""

    tmpl = TEMPLATES_DIR / "book.toml.template"
    if tmpl.is_file():
        text = tmpl.read_text(encoding="utf-8")
        if "{title}" in text:
            text = text.format(title=title, subject=subject, learner=learner, age=age)
    else:
        text = DEFAULT_TOML.format(
            title=title, subject=subject, learner=learner, age=age
        )

    book.toml_path.write_text(text, encoding="utf-8")
    book.outline_path.write_text(DEFAULT_OUTLINE.format(slug=slug), encoding="utf-8")
    book.sources_path.write_text(DEFAULT_SOURCES, encoding="utf-8")

    for line in book.outline_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- ") and ".md" in line:
            name = line[2:].split()[0].strip()
            if name.endswith(".md"):
                path = book.sections_dir / name
                if not path.exists():
                    path.write_text(
                        f"# {name.replace('.md','').replace('-', ' ').title()}\n\n{PLACEHOLDER}",
                        encoding="utf-8",
                    )

    say(f"Created {book.dir}")
    say(f"  edit {book.toml_path}  (learner profile is the most important part)")
    say(f"  edit {book.outline_path}")
    say(f"  then: python -m openbook write {slug}")
    return book
