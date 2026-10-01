---
name: set-up-model-project
description: Set up a new Python financial modelling project with the standard structure, dependency management, linters, tests and agent instructions. Use when starting a new model or repository.
---

# Setting up a model project

1. **Initialise** the folder with Git (`git init`) and `uv init --package <package>`.
2. **Create the structure:**
   - `<package>/` with one folder per category, each holding `<category>_model.py`,
     `<category>_controller.py` and, if needed, `<category>_view.py`;
   - `<package>/helpers.py` for shared utilities;
   - `tests/` mirroring the package, with `conftest.py` providing a `recorder` fixture
     (the Finance Toolkit's `tests/conftest.py` is a good starting point);
   - `examples/` for notebooks.
3. **Configure `pyproject.toml`:** a minimum Python version, core dependencies under `[project]`,
   development tools (pytest, ruff, codespell, ty) under `[dependency-groups] dev`, and the linter
   settings.
4. **Add `.pre-commit-config.yaml`** with ruff (lint and format), codespell and basic checks, and
   run `uv run pre-commit install`.
5. **Add `.gitignore`** for Python, virtual environments, editor folders and notebook
   checkpoints.
6. **Fill in `AGENTS.md`:** replace every placeholder with the project's own name, commands and
   domain rules.
7. **Run** `uv sync`, `uv run pytest tests` and `uv run pre-commit run --all-files` to confirm
   everything works, then make the first commit.
