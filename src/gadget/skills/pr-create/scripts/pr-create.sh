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

echo "Fetching Issue details from GitHub..."
ISSUE_TITLE=$(gh issue view "${ISSUE_ID}" --json title --jq .title)
ISSUE_URL=$(gh issue view "${ISSUE_ID}" --json url --jq .url)

if [ -z "${ISSUE_TITLE}" ]; then
  echo "Error: Could not fetch title for Issue #${ISSUE_ID}. Is the issue ID correct?"
  exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
  echo "Committing uncommitted changes..."
  git add .
  git commit -m "${ISSUE_TITLE} (Fix #${ISSUE_ID})"
fi

echo "Pushing branch ${BRANCH_NAME}..."
git push -u origin HEAD

echo "Creating PR for Issue #${ISSUE_ID}..."
PR_URL=$(gh pr create --title "${ISSUE_TITLE}" --body "Resolves #${ISSUE_ID}")

echo "Enabling auto-merge..."
gh pr merge "${PR_URL}" --squash --auto

echo "Changing directory to parent repository..."
cd ../..

echo "Removing worktree and cleaning up branches..."
git worktree remove ".worktrees/${BRANCH_NAME}" --force
git branch -D "${BRANCH_NAME}" || true
git push origin --delete "${BRANCH_NAME}" || true

echo "PR created and cleanup completed successfully."
echo ""
echo "=================================================="
echo "Issue URL: ${ISSUE_URL}"
echo "PR URL:    ${PR_URL}"
echo "=================================================="
