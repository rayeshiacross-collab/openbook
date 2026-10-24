"""Paths and global config (stdlib only)."""
from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS_DIR = ROOT / "books"
TEMPLATES_DIR = ROOT / "templates"
GLOBAL_CONFIG = ROOT / "config.toml"


def load_global() -> dict:
    if not GLOBAL_CONFIG.is_file():
        return {"mode": "manual", "model": ""}
    with GLOBAL_CONFIG.open("rb") as f:
        return tomllib.load(f)


def say(msg: str) -> None:
    print(msg, flush=True)
