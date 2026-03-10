---
description: Automatically handles a GitHub issue from branch creation to implementation, AI review, and PR creation using the pr-create skill.
---

> [!IMPORTANT]
> **MANDATORY ISOLATION & ARTIFACT RULES**:
> 1. **Worktree Isolation**: All git and file system operations MUST be executed within a dedicated `.worktrees/<branch-name>` directory. Never modify the main workspace.
> 2. **Relative Paths**: Always use relative paths referenced from the current worktree directory.
> 3. **Artifact Storage**: All generated reports (e.g., `research_report.md`, `design_report.md`, `review_report.md`) MUST be saved strictly in the `tmp/` directory provided in metadata. Never save them in the project root or source directories.

**Workflow Steps:**

1. **Initialization**: Ask the user: "Please provide the GitHub Issue ID or Issue Number you would like me to work on." Wait for their input.
2. **Validation**: Invoke the `@gh-issue` skill to verify the issue and update its status. If verification fails, halt the workflow and inform the user immediately.
3. **Branch Setup**: Determine an appropriate branch name (e.g., `issue-<id>-brief-description`).
4. **Isolation Checkpoint (CRITICAL)**: Run the following command to isolate your work: 
   `git fetch origin main && git worktree add .worktrees/<branch-name> -b <branch-name> origin/main && cd .worktrees/<branch-name>`
   *You MUST verify you are successfully inside the `.worktrees/` directory before proceeding.*
5. **Research (Optional but Recommended)**: If the codebase lacks context or previous attempts failed, invoke the `@research` skill with the issue number.
6. **Design (MANDATORY)**: Invoke the `@design` skill with the issue number. Do NOT skip this step under any circumstances.
7. **Planning**: Based on `tmp/research_report.md` (if available), `tmp/design_report.md`, and the issue content, write a detailed implementation plan.
8. **Implementation**: Implement the code changes exactly according to the plan. *Reminder: Ensure you are still working within the isolated worktree.*
9. **Review**: Once implemented, invoke the `@review` skill with the issue number to analyze your changes.
10. **Iterative Refinement (LOOP)**: Read the `tmp/review_report.md` artifact. If there are issues or items requiring review, refactor the code and repeat step 9 (`@review`). You MUST loop this process until the review artifact explicitly states there are **no issues and no items requiring user review**.
11. **PR Creation**: Only when the review passes completely, invoke the `@pr-create` skill with the issue ID to push the branch, create a PR, and clean up.
12. **Final Output**: Present the final results to the user, strictly including the Issue URL and Pull Request URL outputted by the `@pr-create` skill.