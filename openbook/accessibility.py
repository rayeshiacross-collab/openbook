"""Accessibility prompt blocks from learner profile (stdlib only)."""
from __future__ import annotations

from .book import Book


def accessibility_block(book: Book) -> str:
    parts = []
    if book.get("dyslexia_support"):
        parts.append(
            "DYSLEXIA SUPPORT: Use short sentences and short paragraphs. Avoid ambiguous "
            "pronouns — repeat the noun. No idioms, metaphors, or sarcasm. Prefer concrete "
            "nouns over abstract ones. Keep tables narrow (3 columns max) with a header row."
        )
    if book.get("visual_support"):
        parts.append(
            "VISUAL SUPPORT: After introducing any spatial or sequential concept, add a "
            "Visual description block. Express relationships as tables where possible."
        )
    if book.get("auditory_support"):
        parts.append(
            "AUDITORY SUPPORT: Write so the text reads well aloud. Spell out units on first "
            "use. Summaries should be TTS-friendly."
        )
    if book.get("hearing_support"):
        parts.append(
            "HEARING SUPPORT: Never convey information by sound cues alone. Use visible text "
            "or numbered visual steps."
        )
    if book.get("adhd_support"):
        parts.append(
            "ADHD SUPPORT: Short sections when attention is short. Concrete example first. "
            "Frequent checkpoints. Numbered lists for multi-step instructions."
        )
    if book.get("autism_support"):
        parts.append(
            "AUTISM SUPPORT: Literal language only. State structure explicitly. Warn before "
            "topic shifts. Define terms at first use."
        )
    if book.get("motor_support"):
        parts.append(
            "MOTOR SUPPORT: Keyboard-only instructions. Label controls by text name, never "
            "by color or position alone."
        )
    if book.get("cognitive_support"):
        parts.append(
            "COGNITIVE SUPPORT: Concrete before abstract. Worked example before the rule. "
            "One-sentence recap at the start of each section."
        )
    style = book.get("attention_style") or ""
    if style == "short":
        cap = book.get("section_max_words") or 600
        parts.append(
            f"ATTENTION STYLE short: cap this section at about {cap} words. "
            "End with a one-sentence takeaway."
        )
    elif style == "long":
        parts.append("ATTENTION STYLE long: sustained reasoning is fine.")
    n = book.get("checkpoint_every_n_paragraphs") or 0
    if n and int(n) > 0:
        parts.append(f"Insert a one-line checkpoint every {n} paragraphs.")
    mods = book.get("preferred_modalities") or []
    if "hands-on" in mods or book.get("hands_on_every_chapter"):
        parts.append(
            "HANDS-ON: Include a Do this activity completable in under 30 minutes."
        )
    if not parts:
        return ""
    return (
        "\n\nACCESSIBILITY ADAPTATIONS (from this book's learner profile):\n"
        + "\n".join("- " + p for p in parts)
        + "\n"
    )
