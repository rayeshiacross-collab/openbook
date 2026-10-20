# OpenBook

**Write a real textbook for your kid — with any AI, for free, in plain files you own.**

You describe a book. OpenBook plans it like a university text, writes it section by section, runs an accuracy-review pass, and typesets a PDF with numbered chapters, worked examples, colored boxes, summaries, graded problem sets, and a separate solutions manual. It also builds **audiobooks**, **dyslexia-friendly layouts**, and **visual-learning extras** when your child's profile calls for them.

No subscriptions. No API keys required. Nothing leaves your machine unless you choose a cloud AI. Every chapter is a Markdown file in a repo that belongs to you.

Designed for **every parent**: a mom in rural Louisiana, a dad in Tokyo, a grandparent with a laptop and a free ChatGPT account. You do not need to be technical. You do not need to know LaTeX, Git, or anything about how AI works.

## Who it's for

- A parent who wants a textbook tailored to **one specific child** — their age, reading level, language, attention style, and any learning difference (dyslexia, ADHD, autism, hearing or vision impairment, motor or cognitive support needs).
- A teacher building a custom curriculum unit.
- A homeschooler who wants university rigor without university price.
- Anyone who wants to understand how a textbook gets made.

## Three ways to run it (same files, interchangeable)

| Mode | Cost | Who it's for |
|---|---|---|
| **Agent** (Claude Code, Codex, Gemini CLI, Cursor...) | Uses the plan you already have | Fully automatic. The agent reads `AGENTS.md` and loops through the book itself. |
| **Copy-paste** (`manual`) | Free with any chatbot, even free tiers | Grandma's house, or anyone with only a chat window. The tool writes a prompt; you paste it into ChatGPT/Claude/Gemini and paste the reply back. |
| **API / local model** | Local (Ollama, LM Studio) is free; API keys are pay-per-use | Hands-off bulk drafting. Edit `config.toml`. |

Start on one computer, continue on another. Progress is just files — nothing is lost between modes.

## Quick start (five minutes)

**Windows:** open PowerShell in the repo folder and run `py -m openbook doctor`.
**Mac / Linux:** open a terminal and run `python -m openbook doctor`.

```
python -m openbook new my-book --title "My Book" --subject "The subject" --learner "Ada" --age 11
```

Then edit `books/my-book/book.toml` — this is where you describe **your child**. The learner profile is the most important part of the file. Write what you know in plain language:

```
learner_notes = "Dyslexic. Reads at a 5th-grade level but gets adult ideas fast. Short sentences. Lots of examples."
dyslexia_support = true
attention_style = "short"
```

No jargon required. "She gets bored after two pages" is a valid profile. The AI translates it into concrete writing and layout rules.

```
python -m openbook outline my-book      # read and edit the table of contents
python -m openbook write my-book        # drafts every section (resumable)
python -m openbook review my-book       # accuracy-review pass
python -m openbook build my-book        # PDF + solutions manual
python -m openbook status my-book       # progress, page estimate, open [VERIFY] flags
python -m openbook audio my-book        # chapter audiobooks (free TTS: espeak + pyttsx3)
```

With an agent, skip all of that and just say: *"Read AGENTS.md. Create a book on X for my child Y and write it."*

No PDF engine installed? Push the repo to GitHub — the included workflow builds everything in the cloud (Actions tab, then Artifacts).

## What makes it different

- **Per-book accessibility profiles.** Dyslexia mode (OpenDyslexic font, spacing, contrast), visual-learning extras (detailed visual descriptions, diagram tables), audiobook generation (MP3/M4B per chapter), ADHD pacing, autism-friendly literal language, hearing and motor support, phonics hints. One checkbox or one sentence, and the whole book adapts.
- **University rigor, child-calibrated explanation.** The material stays complete and precise; only the *packaging* changes. Terms get defined, prerequisites get explained the first time they're needed.
- **Honest uncertainty.** Any claim the AI isn't sure about gets tagged `[VERIFY]`. `status` counts them. You check the important ones.
- **A real review pass.** A second, skeptical prompt corrects each section and logs what it couldn't confirm.
- **Your sources, your rules.** List OpenStax, LibreTexts, MIT OpenCourseWare, or anything else in `sources.md` and the AI is told to rely on them.
- **Everything is plain text.** Grep it, diff it, back it up, hand it to another AI next month. No lock-in.

## Honest limits

- AI-written books have **no human editors or peer reviewers**. Check anything important — especially math, science, and medicine — with a qualified person or trusted reference, starting with every `[VERIFY]`.
- A 1,000-page book is roughly 300+ sections. Time depends on your usage limits: a few days is realistic for a mid-size book with an agent; longer by copy-paste.
- Image-free by design: the AI describes visuals in prose and tables. Add your own figures if you like. (Visual-support mode adds detailed visual-description blocks to help with this.)
- No back-of-book index yet (per-chapter Key Terms glossaries are included).
- Don't paste in copyrighted textbooks to be reworded. Use openly licensed sources (credit them) and original writing.

## Layout

```
config.toml            which AI writes (manual / API / local)
AGENTS.md CLAUDE.md    instructions for AI agents
openbook/              the tool (Python standard library only, 3.11+)
templates/             PDF styling, box types, dyslexia/visual modes
books/<name>/          book.toml  outline.md  sources.md  sections/  review/  output/
skill/                 Claude skill that teaches Claude to run this repo
tests/                 offline test: python -m unittest tests.test_pipeline
.github/workflows/     cloud PDF builds
```

## License

MIT. Do whatever you want with it. Credit is appreciated, not required. The code cannot be relicensed to restrict others — MIT's terms are irrevocable.

## Contributing

Issues and pull requests welcome. The core rule: **keep it dependency-free** (Python stdlib only) and **keep every chapter a plain file**. If a change breaks either of those, it doesn't belong.
