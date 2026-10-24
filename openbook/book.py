"""Book object: loads book.toml and resolves paths."""
from __future__ import annotations

import re
import tomllib
from pathlib import Path

from .config import BOOKS_DIR

PLACEHOLDER = "<!-- OPENBOOK: write this section -->\n"


class Book:
    def __init__(self, slug: str, root: Path | None = None):
        self.slug = _slugify(slug)
        self.dir = (root or BOOKS_DIR) / self.slug
        self.toml_path = self.dir / "book.toml"
        self.outline_path = self.dir / "outline.md"
        self.sources_path = self.dir / "sources.md"
        self.sections_dir = self.dir / "sections"
        self.review_dir = self.dir / "review"
        self.out_dir = self.dir / "output"
        self._data: dict = {}
        if self.toml_path.is_file():
            with self.toml_path.open("rb") as f:
                self._data = tomllib.load(f)

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def __getitem__(self, key: str):
        return self._data[key]

    @property
    def title(self) -> str:
        return str(self.get("title") or self.slug)

    def ensure_dirs(self) -> None:
        for p in (self.dir, self.sections_dir, self.review_dir, self.out_dir):
            p.mkdir(parents=True, exist_ok=True)

    def section_files(self) -> list[Path]:
        if not self.sections_dir.is_dir():
            return []
        return sorted(self.sections_dir.glob("*.md"))

    def section_status(self) -> list[tuple[str, str]]:
        out = []
        for p in self.section_files():
            text = p.read_text(encoding="utf-8")
            if not text.strip():
                st = "empty"
            elif PLACEHOLDER in text:
                st = "placeholder"
            else:
                st = "done"
            out.append((p.name, st))
        return out


def _slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "book"
