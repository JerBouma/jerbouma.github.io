# GitHub Copilot

All project instructions live in `AGENTS.md` at the root of the repository, so every agent
follows the same rules. Read it and follow it for every task. Step-by-step instructions for
recurring tasks are in `.claude/skills/<name>/SKILL.md`.

The most important rules, in short:

- Calculations only in `*_model.py`, as pure functions with type hints and a docstring that
  states the formula. Data selection in `*_controller.py`, plots in `*_view.py`.
- Never decide a financial definition, unit, period or missing-data treatment silently.
- Every function gets a test; never rewrite recorded test output to make a test pass.
- Run `uv run pytest tests` and `uv run pre-commit run --all-files` before finishing.
