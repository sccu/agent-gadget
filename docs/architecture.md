# Architecture

This document describes the high-level architecture of `agent-gadget`.

---

## Project Layout

```
agent-gadget/
├── GROUND_RULES.md          # Foundational project rules (Symlink to src/gadget/GROUND_RULES.md)
├── AGENTS.md                # Agent skills & workflows spec (Symlink to src/gadget/AGENTS.md)
├── GEMINI.md / GEMINI-COMPACT.md / CLAUDE.md    # LLM behavioral guidelines
├── README.md                # Getting started & usage overview
├── pyproject.toml           # Build config, dependencies, CLI entry point
├── .worktrees/              # Git worktrees for isolated issue handling
├── docs/                    # Detailed documentation
│   ├── architecture.md      # (this file)
│   └── kb/                  # Knowledge Base for troubleshooting and tips
├── src/gadget/
│   ├── __init__.py
│   ├── cli.py               # CLI entry point (`gadget init`)
│   ├── GROUND_RULES.md      # Original foundational rules (copied on `gadget init`)
│   ├── AGENTS.md            # Original agents spec (copied on `gadget init`)
│   ├── scripts/             # Internal helper scripts
│   │   └── handle-issue.sh
│   ├── skills/              # Bundled skill definitions (copied on `gadget init`)
│   │   ├── audit/SKILL.md
│   │   ├── design/SKILL.md
│   │   ├── gh-issue/SKILL.md
│   │   ├── nobot/
│   │   │   ├── SKILL.md
│   │   │   └── scripts/
│   │   │       ├── chrome_launcher.py
│   │   │       ├── coupang_simulator.py
│   │   │       └── humanoid_interactor.py
│   │   ├── pr-create/
│   │   │   ├── SKILL.md
│   │   │   └── scripts/
│   │   │       └── pr-create.sh
│   │   ├── research/SKILL.md
│   │   └── review/SKILL.md
│   └── workflows/           # Bundled workflow definitions
│       └── handle-issue.md
├── .agents/                 # Active agent config (installed by `gadget init`)
│   ├── skills/              # Symlink or copy of src/gadget/skills
│   └── workflows/           # Symlink or copy of src/gadget/workflows
└── tests/
    └── test_dummy.py        # Placeholder test for pre-commit hook
```

## Dependency Direction

```
GROUND_RULES.md  (rules)
       ↓
AGENTS.md / docs/  (documents)
       ↓
src/ / tests/  (code & config)
```

Fixes should propagate **upstream**: if code is wrong because a document is ambiguous, fix the document first.

## CLI Architecture

The `gadget` CLI is a single-command tool registered via `pyproject.toml`:

```
[project.scripts]
gadget = "gadget.cli:main"
```

### `gadget init`

Copies bundled skills and workflows from the package (`src/gadget/skills/`, `src/gadget/workflows/`) into the target project's `.agents/` directory.

**Key functions in `cli.py`:**

| Function | Responsibility |
|----------|---------------|
| `main()` | Argument parsing, command dispatch |
| `init_command()` | Orchestrates the install of skills and workflows |
| `install_items()` | Copies a source directory to target; handles `--force` |
| `get_existing_items()` | Detects conflicts between source and target |
| `remove_items()` | Safely removes items before force-overwrite |

## Testing Strategy

- **Framework**: pytest
- **Pre-commit**: A local hook runs `pytest` on every commit (see `.pre-commit-config.yaml`).
- **Current tests**: `tests/test_dummy.py` — a placeholder assertion to verify the hook works.
