---
title: Working with AI
seo_title: Financial Modelling with AI Coding Assistants
excerpt: "How to set up a financial modelling project for AI coding assistants: instruction files like CLAUDE.md and AGENTS.md, rules, Skills, hooks and MCP servers, and a workflow that keeps you in control."
description: "Set up a Python financial model for AI coding assistants with CLAUDE.md, AGENTS.md, rules, Skills, hooks and MCP servers, and keep every result verifiable."
author_profile: false
permalink: /modelling/working-with-ai
classes: wide-sidebar
sidebar:
    nav: "modelling"
---

{% include mermaid.html %}

The previous pages explain each part of a financial model and how to work on it with an assistant. This page brings that together: how to set up your project so that an AI coding assistant such as Claude Code, GitHub Copilot, Cursor or Codex builds the model the way you designed it, and in a way you can trust.

An assistant that works inside your project reads files, runs commands and makes changes on its own. How well it does that depends far less on how cleverly you phrase a request and far more on the context it has: what the project is, how it is structured, which conventions apply and how to check its own work. All of that can be written down in a few files that live in your repository, next to the code. These files are plain text, they are versioned with Git and they work for every colleague who uses the same tools.

{: .notice--info}
**Tools change quickly, the ideas don't.** File names and features differ per tool and evolve fast, so check the documentation of the assistant you use. The concepts on this page (instructions, rules, skills, automatic checks and data connections) apply to all of them.

{: .notice--info}
**Prefer to start from working files?** The [agent kit](/modelling/introduction#the-agent-kit) contains everything on this page, ready to copy into your repository: an `AGENTS.md` with the rules from this guide, the matching files for Claude Code, GitHub Copilot, Cursor and Gemini CLI, four skills and a hook. [Download it here](/assets/files/financial-modelling-agent-kit.zip).

## The Building Blocks

Most AI coding assistants now support the same set of building blocks. Each has its own job:

| Building block | What it is | When it is used |
|:--|:--|:--|
| **Instruction file** | A Markdown file describing the project, its structure and conventions (`CLAUDE.md`, `AGENTS.md`) | Read at the start of every session |
| **Rules** | Short, targeted instructions that apply to specific files or folders | When the assistant works on matching files |
| **Skills** | A folder with step-by-step instructions (and optional scripts) for a recurring task | Loaded only when the task matches the skill's description |
| **Hooks** | Commands that run automatically at fixed moments, such as after every edit | Always, without the assistant deciding |
| **MCP servers** | Connections to external tools and data, such as financial data or a database | When the assistant needs that data or tool |

The difference between them is mostly about *when* the information is used. Instructions are always loaded, so they should be short. Rules and skills are loaded only when relevant, so they can be more detailed. Hooks don't depend on the assistant at all, which makes them the right place for anything that must always happen.

## Instruction Files

The instruction file is the most important one. It is the README for your assistant: what it would need to know on its first day in the project. Claude Code reads `CLAUDE.md`; Codex, Cursor, Copilot and many others read `AGENTS.md`, an open convention shared by several tools. GitHub Copilot also reads `.github/copilot-instructions.md`. If you use several tools, keep one file as the source and point the others to it.

Place it at the root of the repository. Most tools also read instruction files in subfolders when they work there, and a personal file in your home folder for preferences that apply to all your projects. In Claude Code, running `/init` drafts a first version based on your codebase, which you can then correct.

A good instruction file for a financial model is short and specific. For example:

```markdown
# Finance Model

Python package that calculates financial ratios and performance metrics
from company financial statements.

## Structure
- `financemodel/<category>/<category>_model.py`: pure calculation functions.
  Inputs are pd.Series or floats, never full DataFrames with column names.
- `financemodel/<category>/<category>_controller.py`: selects the data and calls
  the model functions. No calculations here.
- `financemodel/helpers.py`: shared utilities such as growth calculations.
- `tests/` mirrors the package; every model function has a matching test.

## Commands
- Install: `uv sync`
- Test: `uv run pytest tests`
- Lint: `uv run pre-commit run --all-files`

## Conventions
- PEP 8, type hints on every function, Google-style docstrings that include
  the formula.
- Percentages are stored as fractions (0.25, not 25).
- Never rewrite recorded test output (`--record-mode=rewrite`) without
  showing me the difference first.
```

Notice what is in there: the structure from [Structure your Model](/modelling/structure-your-model), the commands from [Setting up your Project](/modelling/setting-up-your-project), the conventions from [Build your Model](/modelling/build-your-model) and the testing rule from [Test your Model](/modelling/test-your-model). You can only write a file like this if you understand those parts, and an assistant can only follow them if they are written down.

Some guidelines for writing it:

- **Keep it short.** It is loaded in every session and competes with the actual task for the assistant's attention. A page is plenty; move details into rules or skills.
- **Write rules, not essays.** "Percentages are stored as fractions" is more useful than a paragraph on why consistency matters.
- **Include the commands.** An assistant that knows how to run the tests will run them.
- **Update it when it gets something wrong.** If the assistant keeps putting calculations in a controller, that is a missing line in this file.

## Rules

Rules are instructions that only apply to part of the project. They keep the main instruction file short, because the details for, say, the model layer are only loaded when the assistant works on model files. Cursor stores them in `.cursor/rules/`, GitHub Copilot in `.github/instructions/`, and in Claude Code you can place a `CLAUDE.md` in a subfolder that only applies to the files in that folder.

A rule usually has a small header that says which files it applies to, followed by the instructions. For example, a Cursor rule for all model files (Copilot uses `applyTo` instead of `globs`, but the idea is the same):

```markdown
---
description: Conventions for calculation functions
globs: financemodel/**/*_model.py
---

- Functions are pure: no data loading, no plotting, no printing.
- Accept pd.Series, pd.DataFrame or float and return the same shape.
- Do not drop or fill missing values silently; let NaN propagate.
- Put the formula in the docstring, with a source for non-standard definitions.
- Avoid magic numbers: a risk-free rate or a number of trading days is a
  parameter with a documented default.
```

Rules are where your domain knowledge goes. Which definition of a ratio your team uses, how quarterly and annual data are combined, or which data sources are allowed are exactly the decisions an assistant cannot make for you.

## Skills

A skill is a recurring task written down once, so the assistant can perform it the same way every time. It is a folder containing a `SKILL.md` file with a name, a description and step-by-step instructions, and optionally scripts or templates the assistant can use. Agent Skills started in Claude and are now an open format that other tools support as well. In Claude Code, project skills live in `.claude/skills/<skill-name>/SKILL.md`.

The key difference with an instruction file is that a skill is not always loaded. The assistant only sees its short description and loads the full instructions when a task matches it. That means you can have many detailed skills without cluttering every session.

For a financial model, adding a new ratio is a typical candidate:

```markdown
---
name: add-financial-ratio
description: Add a new financial ratio to the model, including the controller
  method, test and documentation. Use when asked to add or implement a ratio.
---

# Adding a financial ratio

1. Confirm the exact definition with the user if more than one is common
   (e.g. which earnings measure for a P/E ratio). Do not choose silently.
2. Add a pure function to the right `<category>_model.py`, with type hints
   and a docstring that states the formula.
3. Add a controller method in `<category>_controller.py` that selects the
   inputs from the statements and calls the model function. Support the
   existing `growth`, `lag` and `rounding` parameters.
4. Add a test in the mirrored test file with small, hand-checkable inputs.
   Calculate one expected value by hand and show it in your summary.
5. Run `uv run pytest tests` and `uv run pre-commit run --all-files`.
6. Summarise: the formula used, the files changed and the hand-checked value.
```

A skill like this turns your understanding of the model into a repeatable process. Good candidates are tasks you explain more than once: adding a metric, adding a data source, updating a model after a dependency changes, or preparing a release.

## Hooks

Instructions, rules and skills are guidance: the assistant follows them most of the time. Hooks are not guidance. They are commands that the tool itself runs at a fixed moment, for example after every file edit or before the assistant finishes. That makes them the right place for anything that must happen every time.

In Claude Code, hooks are configured in `.claude/settings.json`. For example, to format and lint every Python file right after the assistant edits it:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "uv run ruff format . && uv run ruff check --fix ." }
        ]
      }
    ]
  }
}
```

The [pre-commit hooks](/modelling/setting-up-your-project#setting-up-linters) you already have play the same role at commit time. Together they mean that style and basic correctness are checked automatically, so your review can focus on what matters: whether the finance is right.

## MCP Servers

The Model Context Protocol (MCP) is a standard way to connect an assistant to external tools and data. An MCP server can give the assistant access to a database, a documentation source or financial data. In Claude Code, servers shared by a project are listed in a `.mcp.json` file in the repository.

For financial modelling this is useful in two ways. While building, an assistant can look up real data to check its work, for example comparing a calculated ratio with the reported figures. And for analysis, it can run calculations directly. The [Finance Toolkit MCP server](/projects/financetoolkit/mcp) is an example: it gives assistants access to the same 500+ transparent calculations as the Python package, so the numbers in a conversation come from documented formulas rather than from the model's memory.

Treat MCP servers like any other dependency: only connect servers you trust, and be careful with servers that can change data rather than only read it.

## A Workflow that Keeps You in Control

With these files in place, a typical change looks like this:

<div class="mermaid">
flowchart LR;
A["Describe a small task"] --> B["Assistant plans"]
B --> C["You check the plan"]
C --> D["Assistant changes code"]
D --> E["Hooks lint and format"]
E --> F["Tests run"]
F --> G["You review the diff"]
G --> H["Commit"]
</div>

A few habits make the biggest difference:

- **Keep tasks small.** "Add the operating margin" works better than "build the profitability module". Small tasks give small diffs that you can actually review.
- **Ask for a plan first.** Most tools have a planning mode. Checking a plan takes a minute and catches a wrong definition before any code is written.
- **Let it run the tests, but read the result yourself.** A passing test suite only means something if the expected values are right, as explained in [Test your Model](/modelling/test-your-model#tests-and-ai-assistants).
- **Review the diff with the checklist** from [Reviewing AI-Written Code](/modelling/build-your-model#reviewing-ai-written-code): formula, units, periods, missing data and hidden assumptions.
- **Turn corrections into files.** When you correct the assistant twice for the same thing, add it to the instruction file, a rule or a skill. Over time the project gets better at explaining itself.

{: .notice--info}
**Understanding is still the job.** An assistant with good instructions can do most of the typing. Deciding which definition is right, noticing that a result is implausible and knowing what a test should expect still depend on you. That is why the rest of this guide explains each component of a model in depth: it is what lets you write good instructions, and what lets you judge the outcome.

Have suggestions? This entire website is open-source, so feel free to contribute [here](https://github.com/JerBouma/jerbouma.github.io){: target="_blank"}!
