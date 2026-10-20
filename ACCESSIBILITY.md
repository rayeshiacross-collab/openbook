# Accessibility in OpenBook

Every book gets its own learner profile in `book.toml`. The AI reads it and adapts writing, pacing, and layout. No jargon required from the parent.

## Profile fields

| Field | What it does |
|---|---|
| `learner_notes` | One plain sentence. "Dyslexic, reads at 5th-grade level, gets adult ideas fast." |
| `reading_level` | e.g. `grade 3`, `grade 8`, `adult` |
| `attention_style` | `short` / `standard` / `long` / `variable` |
| `dyslexia_support` | OpenDyslexic font, wide spacing, high contrast, no justified text |
| `visual_support` | Detailed visual-description blocks, diagram tables, color-coded boxes |
| `auditory_support` | Text written to read well aloud; audiobook generation enabled |
| `hearing_support` | Visual-first instructions, no audio-only cues |
| `adhd_support` | Short sections, immediate examples, frequent checkpoints |
| `autism_support` | Literal language, no idioms, predictable structure, topic-shift warnings |
| `motor_support` | Keyboard-only navigation, text labels not colors |
| `cognitive_support` | Concrete before abstract, worked examples before rules |
| `phonics_support` | Syllable-break hints on new words, irregular-word flags |
| `preferred_modalities` | `text`, `audio`, `visual`, `hands-on` |
| `hands_on_every_chapter` | Each chapter closes with a do-this activity |

## Audiobook engines (free)

- **espeak-ng / espeak** — offline, works anywhere, robotic but reliable
- **pyttsx3** — wraps platform voices (Windows SAPI5, Mac NSSpeech, Linux espeak)

Run `python -m openbook audio <slug>`. If the first engine fails mid-chapter, it switches to the other automatically and tells you which produced which file. Install ffmpeg to merge chapters into one audiobook.

## Layout modes

- `--dyslexia` on build: OpenDyslexic font (or TeX Gyre Pagella fallback), 1.35 line spacing, ragged right, high-contrast boxes
- `--visual` on build: larger type, wider margins, color-forward boxes

## Phonics overlay

When `phonics_support = true`, new multisyllable words get a phonetic hint in parentheses at first use, e.g. `photosynthesis (fo-to-SIN-thuh-sis)`. Irregular words get flagged. It's a hint layer, not a rewrite.
