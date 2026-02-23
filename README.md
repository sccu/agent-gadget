# agent-gadget

**agent-gadget** is an agent-first development framework. 
It operates on a strict dependency direction: `rule → document → code`. 
Therefore, if an agent generates incorrect documentation or code, the intended resolution is to improve the upstream `rule` or `document` to prevent the same issue from reoccurring, rather than merely fixing the resulting code.

This project is built as a configurable Python project using `pyproject.toml`.

## Table of Contents
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
- [Agent Workflows and Skills](#agent-workflows-and-skills)
  - [Issue Creation](#1-issue-creation)
  - [Issue Resolution](#2-issue-resolution-workflow)
  - [PR Review and Merging](#3-pr-review-and-merging-human-in-the-loop)
  - [Worktree Cleanup](#4-worktree-cleanup)

---

## Getting Started

### Installation

To install the CLI in editable mode for development:

```bash
pip install -e ".[dev]"
```

> **Note:** If the installation hangs or takes unusually long, it might be due to a system keyring issue (e.g., on macOS). You can bypass the keyring block by running:
> ```bash
> PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring pip install -e ".[dev]"
> ```

### Basic Usage
After installation, you can run the initialization command to set up the agent environment:

```bash
gadget init
```

---

## Agent Workflows and Skills

This project leverages agentic capabilities for automated development workflows. 

### 1. Issue Creation
**Trigger:** `@github-issue <user_prompt>`

Use this command to generate a new GitHub issue. The agent will read your prompt and the project context, ask any necessary clarifying questions, and scaffold a professional GitHub issue for you.

### 2. Issue Resolution Workflow
**Trigger:** `/handle-issue #<issue-id>`

This workflow fully automates the development lifecycle for a specific issue:
1. Reads the content and context of the specified issue.
2. Generates an appropriate branch name containing the issue identifier.
3. Sets up a new Git worktree and branch to safely isolate development.
4. Implements the necessary codebase changes based on its analysis.
5. Invokes the `@review` QA skill once the initial implementation is ready.
6. Iteratively refactors the code based on the feedback from the generated `review_results.md` artifact until all quality standards are met.

### 3. PR Review and Merging (Human-in-the-loop)
Once the automated workflow opens a Pull Request, a human developer should review the code changes and manually merge the PR.

### 4. Worktree Cleanup
**Trigger:** Ask the agent to *"clean up the worktree"*

After the PR is merged, you can request the agent to clean up the environment. The agent will automatically remove the temporary worktree directory and delete both the local and remote branches used for the issue.
