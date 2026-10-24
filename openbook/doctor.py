"""Environment checks — fail closed with clear messages."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from .config import ROOT, say


def run() -> int:
    ok = True
    say(f"OpenBook doctor  (python {sys.version.split()[0]})")
    say(f"ROOT={ROOT}")

    if sys.version_info < (3, 11):
        say("FAIL: Python 3.11+ required")
        ok = False
    else:
        say("OK   Python version")

    for mod in ("tomllib", "pathlib", "re", "json", "subprocess"):
        try:
            __import__(mod)
            say(f"OK   import {mod}")
        except ImportError:
            say(f"FAIL import {mod}")
            ok = False

    for name, hint in (
        ("espeak-ng", "or espeak — free offline TTS"),
        ("espeak", "fallback TTS"),
        ("ffmpeg", "merge chapter audio / convert"),
        ("pandoc", "optional Markdown→PDF"),
        ("xelatex", "optional LaTeX PDF engine"),
    ):
        p = shutil.which(name)
        if p:
            say(f"OK   {name} → {p}")
        else:
            say(f"---- {name} not found ({hint})")

    try:
        import pyttsx3  # noqa: F401
        say("OK   pyttsx3 (optional TTS)")
    except ImportError:
        say("---- pyttsx3 not installed (pip install pyttsx3 --user)")

    books = ROOT / "books"
    if books.is_dir():
        n = len([p for p in books.iterdir() if p.is_dir()])
        say(f"OK   books/ ({n} book dir(s))")
    else:
        say("---- books/ missing (created on first `new`)")

    if ok:
        say("\nDoctor: PASS — ready for `python -m openbook new ...`")
        return 0
    say("\nDoctor: FAIL — fix items above")
    return 1
