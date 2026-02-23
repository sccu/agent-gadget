# Gadget

A basic Python project using `pyproject.toml`.

## Installation

To install the CLI in editable mode for development:

```bash
pip install -e .
```

## Usage

After installation, you can run the CLI tool:

```bash
gadget init
```

### Agent Workflows and Skills

This project leverages agentic capabilities for automated development workflows. 

#### 1. Issue Creation (`@github-issue <user_prompt>`)
Use this command to generate a new GitHub issue. The agent will read your prompt and the project context, ask any necessary clarifying questions, and scaffold a professional GitHub issue for you.

#### 2. Issue Resolution Workflow (`/handle-issue #<issue-id>`)
This workflow fully automates the development lifecycle for a specific issue:
1. Reads the content and context of the specified issue.
2. Generates an appropriate branch name containing the issue identifier.
3. Sets up a new Git worktree and branch to safely isolate development.
4. Implements the necessary codebase changes based on its analysis.
5. Invokes the `@review` QA skill once the initial implementation is ready.
6. Iteratively refactors the code based on the feedback from the generated `review_results.md` artifact until all quality standards are met.

#### 3. PR Review and Merging (Human-in-the-loop)
Once the automated workflow opens a Pull Request, a human developer should review the code changes and merge the PR.

#### 4. Worktree Cleanup
After the PR is merged, you can simply ask the agent to **"clean up the worktree"**. The agent will automatically remove the temporary worktree directory and delete both the local and remote branches used for the issue.
