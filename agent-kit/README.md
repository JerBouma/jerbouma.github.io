# Financial Modelling Agent Kit

Instructions, rules and skills that teach any AI coding agent how to build financial models the
way the [Financial Modelling with Python](https://www.jeroenbouma.com/modelling/introduction)
guide describes: a Model-View-Controller structure, transparent calculations, recorded tests and
no silent financial choices.

## Installation

1. Copy everything in this folder, including the hidden folders (`.claude`, `.cursor`,
   `.github`), into the root of your repository. If a file already exists, merge the content.
2. Open `AGENTS.md` and replace every `<placeholder>` with your own project's details. Delete
   what does not apply and add your own domain rules.
3. Remove the files for tools you don't use (see the table below). Keep `AGENTS.md`.

## What is in it

`AGENTS.md` holds all instructions. Every other file points to it, so you only maintain one set
of rules.

| File | Used by |
|:--|:--|
| `AGENTS.md` | The instructions themselves. Read natively by Codex, Cursor, GitHub Copilot, Windsurf, Zed, Jules, Aider and many other agents |
| `CLAUDE.md` | Claude Code (imports `AGENTS.md`) |
| `GEMINI.md` | Gemini CLI (points to `AGENTS.md`) |
| `.github/copilot-instructions.md` | GitHub Copilot in VS Code, JetBrains and on github.com |
| `.github/instructions/model-layer.instructions.md` | GitHub Copilot, for `*_model.py` files only |
| `.cursor/rules/project.mdc` | Cursor, always on |
| `.cursor/rules/model-layer.mdc` | Cursor, for `*_model.py` files only |
| `.claude/skills/*/SKILL.md` | Agent Skills: loaded automatically by tools that support them (such as Claude Code and GitHub Copilot); `AGENTS.md` tells other agents where to find them |
| `.claude/settings.json` | Claude Code hook that formats and lints every edited file |

## Skills

| Skill | What it does |
|:--|:--|
| `add-financial-metric` | Adds a ratio, indicator or model: definition, model function, controller method, test and documentation |
| `write-model-tests` | Writes tests that mirror the model and record expected outputs, verified by hand |
| `review-model-change` | Reviews a change on formula, units, periods, missing data, hidden assumptions, structure and tests |
| `set-up-model-project` | Sets up a new project with the structure, uv, linters, tests and these instructions |

## Keep in mind

Tools and their file conventions change quickly; check the documentation of the agent you use.
The instructions are a starting point: the more of your own model's rules you add, the better
an agent follows them. Read the guide for the reasoning behind every rule.

MIT licensed. Use, adapt and share freely.
