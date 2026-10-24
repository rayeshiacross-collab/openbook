"""Section writing helpers and AI-mode prompts."""
from __future__ import annotations

from pathlib import Path

from .accessibility import accessibility_block
from .book import Book, PLACEHOLDER
from .config import load_global, say
from .phonics import phonics_hint_block


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def is_done(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    return bool(text.strip()) and PLACEHOLDER not in text


def section_prompt(book: Book, section_path: Path) -> str:
    outline = read(book.outline_path)
    sources = read(book.sources_path)
    title = section_path.stem
    acc = accessibility_block(book)
    phon = phonics_hint_block(book)

    return f"""You are writing one section of a textbook.

Book title: {book.title}
Subject: {book.get('subject', '')}
Level: {book.get('level', 'university')}
Learner: {book.get('learner_name', '')} (age {book.get('learner_age', '')})
Learner notes: {book.get('learner_notes', '')}
Voice: {book.get('voice', '')}
Notes: {book.get('notes', '')}

Section file: {section_path.name}
Section id: {title}

{acc}
{phon}

Sources the author wants preferred:
{sources or '(none listed)'}

Outline (for context; write ONLY this section):
{outline}

Rules:
- University rigor; calibrate explanation to the learner profile.
- Define terms at first use. Prefer concrete examples before abstract rules.
- Tag uncertain factual claims with [VERIFY].
- Do not invent citations. Prefer listed sources.
- Output Markdown only for this section (heading + body). No surrounding commentary.
- Target about {book.get('words_per_section') or 1200} words unless attention_style=short.

Write the complete section now.
"""


def write_sections(book: Book, *, only: str | None = None, force: bool = False) -> None:
    mode = load_global().get("mode", "manual")
    prompts_dir = book.dir / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    files = book.section_files()
    if only:
        files = [p for p in files if only in p.name]
    if not files:
        say("No section files. Edit outline.md and re-run new, or add sections/*.md")
        return

    for path in files:
        if is_done(path) and not force:
            say(f"  skip (done): {path.name}")
            continue
        prompt = section_prompt(book, path)
        prompt_path = prompts_dir / (path.stem + ".prompt.txt")
        prompt_path.write_text(prompt, encoding="utf-8")
        if mode == "manual":
            say(f"  prompt → {prompt_path}")
            say(f"    paste into your AI, then save the reply to {path}")
        else:
            say(f"  prompt ready: {prompt_path} (mode={mode})")

    say("Writing is resumable. Finished sections are left untouched unless --force.")
