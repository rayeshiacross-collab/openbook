"""Offline tests — no network, no AI calls."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from openbook.book import Book, PLACEHOLDER
from openbook.writer import is_done, section_prompt
from openbook.build import assemble
from openbook.review import count_verify
from openbook.doctor import run as doctor_run


class PipelineTests(unittest.TestCase):
    def test_doctor_pass(self):
        self.assertEqual(doctor_run(), 0)

    def test_assemble_and_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            slug = "demo-book"
            bdir = Path(tmp) / slug
            bdir.mkdir()
            (bdir / "sections").mkdir()
            (bdir / "book.toml").write_text(
                'title = "Demo"\nsubject = "Test"\nlearner_name = "Ada"\n'
                "dyslexia_support = true\n",
                encoding="utf-8",
            )
            (bdir / "outline.md").write_text("# Outline\n", encoding="utf-8")
            (bdir / "sources.md").write_text("# Sources\n", encoding="utf-8")
            sec = bdir / "sections" / "01-01-intro.md"
            sec.write_text(
                "# Introduction\n\nWater boils at 100 C [VERIFY].\n\nMore text.",
                encoding="utf-8",
            )
            book = Book(slug, root=Path(tmp))
            self.assertTrue(is_done(sec))
            self.assertEqual(count_verify(sec.read_text()), 1)
            prompt = section_prompt(book, sec)
            self.assertIn("DYSLEXIA SUPPORT", prompt)
            text, sols, missing = assemble(book)
            self.assertIn("Introduction", text)
            self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
