---
title: Git 관련 트러블슈팅 및 팁
description: Git Worktree 환경의 브랜치명 조회와 조건 처리 팁
tags: [git, troubleshooting, worktree, script]
---

# Git 관련 트러블슈팅 및 팁

## Git Worktree 환경에서 현재 브랜치 이름 가져오기

Git Worktree 환경에서 개발을 진행하거나 셸 스크립트를 작성할 때는 현재 브랜치의 이름을 정확하고 안전하게 가져오는 것이 중요합니다.

### 1. 권장 방식: `git branch --show-current`

가장 안전하고 추천하는 방식입니다.

```bash
BRANCH_NAME=$(git branch --show-current)

# Fail-fast 예외 처리
if [ -z "$BRANCH_NAME" ]; then
  echo "Error: Not currently on any branch. Are you in a detached HEAD state?"
  exit 1
fi
```

**장점과 특징:**
- 명령어의 목적이 명확하여 가독성이 매우 뛰어납니다.
- **Detached HEAD 상태에서의 안정성**: 브랜치가 아닌 특정 커밋을 직접 체크아웃한 상태(Detached HEAD)에서 스크립트가 실행될 경우, 이 명령어는 **빈 문자열을 반환**합니다. 덕분에 `if [ -z "$BRANCH_NAME" ];` 형태로 손쉽게 예외 처리가 가능하며 프로젝트 룰인 **Fail-fast 시스템**을 구축하기에 안성맞춤입니다.
- Git 2.22 버전 이상에서 사용 가능합니다.

### 2. 권장하지 않는 방식: `git rev-parse --abbrev-ref HEAD`

기존의 전통적인 방식이지만 엣지 케이스에서 문제가 발생할 수 있습니다.

**단점과 잠재적 위험:**
- 본래 `rev-parse` 명령어의 목적이 객체 해석을 위한 것이므로 우회적으로 브랜치명을 추출하는 것에 가깝습니다.
- **Detached HEAD 상태에서의 위험성**: 해당 명령어는 Detached HEAD 상태일 때 빈 문자열이 아닌 **문자열 `"HEAD"`를 반환**합니다. 이를 셸 스크립트에서 별다른 처리 없이 사용하면 로컬 혹은 원격 깃 저장소에 문자열 "HEAD"라는 이름의 브랜치로 푸시하거나 처리해버리는 논리적 결함을 유발할 수 있습니다.
