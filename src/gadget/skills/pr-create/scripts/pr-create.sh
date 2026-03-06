#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <issue-id>"
  exit 1
fi

ISSUE_ID=$1
BRANCH_NAME=$(git branch --show-current)

if [ -z "$BRANCH_NAME" ]; then
  echo "Error: Not currently on any branch. Are you in a detached HEAD state?"
  exit 1
fi

echo "Pushing branch ${BRANCH_NAME}..."
git push -u origin HEAD

echo "Creating PR for Issue #${ISSUE_ID}..."
gh pr create --title "$(git log -1 --pretty=%s)" --body "Resolves #${ISSUE_ID}"

echo "Enabling auto-merge..."
gh pr merge --squash --auto

echo "Changing directory to parent repository..."
cd ../..

echo "Removing worktree and cleaning up branches..."
git worktree remove ".worktrees/${BRANCH_NAME}" --force
git branch -D "${BRANCH_NAME}" || true
git push origin --delete "${BRANCH_NAME}" || true

echo "PR created and cleanup completed successfully."
