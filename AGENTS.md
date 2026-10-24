# OpenBook — instructions for AI agents

You are helping a parent write a textbook for one specific child.

1. Read `config.toml` and the target `books/<slug>/book.toml`.
2. The **learner profile** in `book.toml` is the most important input.
3. Prefer open sources in `sources.md`. Tag uncertain facts with `[VERIFY]`.
4. Workflow: doctor → new → edit outline/profile → write → review → build → audio
5. Do not call paid APIs unless the user explicitly configured them.
6. Keep every chapter a plain Markdown file.
