# Design Report: src/gadget/ 내 복제된 핵심 문서 누락 (#45)

## Architecture Overview
이 디자인 리포트는 `docs/architecture.md` 파일의 Project Layout 섹션에 누락된 핵심 문서 정보(`GROUND_RULES.md`와 `AGENTS.md`의 실제 위치 및 심볼릭 링크 여부)를 추가하는 변경 사항을 정의합니다. 프로젝트의 실제 구조와 문서 간의 일관성을 유지하기 위함입니다.

## Component Design
변경할 대상 컴포넌트는 오직 `docs/architecture.md` 문서입니다.

### `docs/architecture.md` 변경 사항:
1. 최상위 디렉토리의 `GROUND_RULES.md`와 `AGENTS.md` 항목에 이들이 `src/gadget/` 내부의 실제 파일을 가리키는 **심볼릭 링크**임을 명시합니다.
2. `src/gadget/` 하위 구조 부분에 `GROUND_RULES.md`와 `AGENTS.md`가 실제 위치하는 원본 파일임을 추가로 명시합니다. (`gadget init` 초기화를 위한 소스)

## Data Flow
데이터 흐름 변경 없음 (단순 문서 업데이트)

## Dependencies
추가 의존성 없음

## Edge Cases & Error Handling
- 문서의 다른 부분이 훼손되지 않도록 정확한 위치(Project Layout 트리 구조)만 수정합니다.

## Step-by-Step Implementation Map
1. `.worktrees/issue-45-missing-core-docs-in-src-gadget/docs/architecture.md` 파일을 엽니다.
2. `GROUND_RULES.md`와 `AGENTS.md`의 설명을 수정하여 심볼릭 링크임을 명시합니다.
3. `src/gadget/` 디렉토리 하위에 원본 `GROUND_RULES.md`와 `AGENTS.md` 파일이 존재함을 추가합니다.
4. 변경 사항을 저장하고 빌드/테스트를 통해 문제가 없는지 확인합니다.