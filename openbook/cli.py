"""OpenBook CLI."""
from __future__ import annotations

import argparse
import sys

from . import __version__
from .audio import generate_audiobook
from .book import Book
from .build import build_book
from .doctor import run as doctor_run
from .new_book import create
from .review import review_book
from .status import status_book
from .writer import write_sections


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="openbook",
        description="Write university-grade textbooks for one learner — plain files you own.",
    )
    p.add_argument("--version", action="version", version=f"openbook {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("doctor", help="Check environment")

    n = sub.add_parser("new", help="Create a book")
    n.add_argument("slug")
    n.add_argument("--title", default="")
    n.add_argument("--subject", default="")
    n.add_argument("--learner", default="")
    n.add_argument("--age", default="")

    o = sub.add_parser("outline", help="Show outline path")
    o.add_argument("slug")

    w = sub.add_parser("write", help="Emit section prompts (resumable)")
    w.add_argument("slug")
    w.add_argument("--only", default="")
    w.add_argument("--force", action="store_true")

    r = sub.add_parser("review", help="Emit accuracy-review prompts")
    r.add_argument("slug")

    b = sub.add_parser("build", help="Assemble Markdown (+ optional PDF)")
    b.add_argument("slug")
    b.add_argument("--dyslexia", action="store_true")
    b.add_argument("--visual", action="store_true")

    s = sub.add_parser("status", help="Progress and [VERIFY] counts")
    s.add_argument("slug")

    a = sub.add_parser("audio", help="Chapter audiobooks (free TTS)")
    a.add_argument("slug")
    a.add_argument("--voice", default="default")
    a.add_argument("--format", default="mp3", choices=["mp3", "wav"])

    args = p.parse_args(argv)

    if args.cmd == "doctor":
        return doctor_run()

    if args.cmd == "new":
        create(
            args.slug,
            title=args.title,
            subject=args.subject,
            learner=args.learner,
            age=args.age,
        )
        return 0

    book = Book(args.slug)
    if not book.toml_path.is_file():
        print(f"Unknown book: {args.slug}", file=sys.stderr)
        return 2

    if args.cmd == "outline":
        print(book.outline_path)
        return 0
    if args.cmd == "write":
        write_sections(book, only=args.only or None, force=args.force)
        return 0
    if args.cmd == "review":
        review_book(book)
        return 0
    if args.cmd == "build":
        build_book(book, dyslexia=args.dyslexia, visual=args.visual)
        return 0
    if args.cmd == "status":
        status_book(book)
        return 0
    if args.cmd == "audio":
        generate_audiobook(book, voice=args.voice, fmt=args.format)
        return 0

    return 1
