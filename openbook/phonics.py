"""Phonics overlay hints for prompts."""
from __future__ import annotations

from .book import Book


def phonics_hint_block(book: Book) -> str:
    if not book.get("phonics_support"):
        return ""
    return (
        "\nPHONICS SUPPORT: On first use of multisyllable or irregular words, "
        "add a simple phonetic hint in parentheses, e.g. photosynthesis "
        "(fo-to-SIN-thuh-sis). Do not rewrite the whole text into phonetic spelling.\n"
    )
