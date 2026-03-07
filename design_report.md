# Design Report: `run_search` 함수 리팩토링 설계

## 1. 개요 (Architecture Overview)
기존 `coupang_simulator.py` 내의 `run_search` 함수는 약 60줄에 달하며, 쿠팡 접속, 센서 스크립트 대기, 웜업, 검색어 입력, 검색 실행, 결과 검증 등 6가지 이상의 동작을 포함하고 있습니다. 이로 인해 50줄 이내의 함수 크기를 유지하라는 Simplicity 규칙을 위배합니다.
본 리팩토링 설계는 이 무거운 단일 함수를 3개의 역할별 비동기 헬퍼 함수로 분리하고, `run_search`는 이들 함수를 호출하는 오케스트레이터로 변경하여 각 함수의 길이를 50줄 미만으로 최적화하며 가독성 및 유지보수성을 극대화합니다.

## 2. 컴포넌트 설계 (Component Design)

새롭게 분리/추가될 함수들의 시그니처 및 역할은 다음과 같습니다. 모두 `async` 로 선언됩니다.

### 2.1 `_navigate_and_check(page: Page) -> None`
- **입력 파라미터**: Playwright의 `page` 객체 (단, 타입 힌팅은 `Page`를 생략하거나 사용할 수 있음. 기존 코드 스타일 준수)
- **리턴 타입**: 반환값 없음 (실패 시 예외 발생)
- **주요 로직**:
  - `https://www.coupang.com` 으로 이동(`wait_until="commit"`)
  - 무작위 시간(3~5초) 대기 (센서 스크립트 대응)
  - 페이지 타이틀 기반 상태 확인 (차단되었을 경우 `RuntimeError` 발생)

### 2.2 `_perform_search(page: Page, interactor: HumanoidInteractor, query: str) -> None`
- **입력 파라미터**: `page` 객체, 초기화된 `interactor` 객체, 검색어 `query`
- **리턴 타입**: 반환값 없음
- **주요 로직**:
  - 인간 모방 동작(warm_up) 실행
  - 검색어 입력창을 기다린 후(timeout 설정) `query` 문자열 타이핑(`human_type`)
  - 무작위 시간 대기 후 검색 버튼 클릭(`human_click`)

### 2.3 `_verify_results(page: Page, query: str) -> bool`
- **입력 파라미터**: `page` 객체, 검색어 `query`
- **리턴 타입**: 검증 성공 시 `True` 반환 (실패 시 예외 발생)
- **주요 로직**:
  - 결과 페이지 로딩을 위해 일정 시간(5초) 대기
  - 변경된 페이지의 URL과 Title 추출
  - 쿠팡의 봇 차단 페이지 여부 확인(`_is_blocked`)
  - 최종 URL에 "search" 문자열 또는 `query`가 포함되어 있는지 검증하고, 그렇지 않을 경우 `RuntimeError` 발생

### 2.4 오케스트레이터: `run_search(query: str, launcher: ChromeLauncher) -> bool`
- **입력/출력**: 기존 시그니처와 동일
- **주요 로직**:
  - `async_playwright` 컨텍스트 및 브라우저 연결 생성
  - 에러 처리(try-except) 블록 구성
  - 순차적으로 `_navigate_and_check`, `_perform_search`, `_verify_results` 호출
  - `_verify_results`의 결과 반환

## 3. 데이터 흐름 (Data Flow)
1. 외부 시스템(메인 루프)이 `run_search(query, launcher)` 호출
2. `run_search` 내부에서 `launcher.connect`를 통해 `browser`, `page` 객체 생성
3. `page` 인스턴스가 `_navigate_and_check`로 전달되어 초기 상태 검증을 거침
4. `page`, `interactor`, `query` 데이터가 `_perform_search`로 전달되어 UI 이벤트를 발생시킴
5. `page`, `query` 데이터를 기반으로 `_verify_results`가 결과 화면을 검증
6. 작업 중 발생한 예외(차단 등)는 각 헬퍼 함수가 즉각 `raise`하고, `run_search`의 통합 `try-except`에서 최종 확인 및 로깅 처리

## 4. 의존성 (Dependencies)
새로운 라이브러리를 추가할 필요가 없으며, 기존에 임포트된 `asyncio`, `random`, `playwright.async_api` 타입을 그대로 활용합니다.

## 5. 예외 및 에지 케이스 핸들링 (Edge Cases & Error Handling)
- **차단 상황**: 기존 방식 모델과 동일하게 빠른 실패(Fail-fast)를 우선합니다. 헬퍼 함수들이 중간에 봇 차단을 감지하거나 예기치 않은 URL 형태를 반환받으면 즉시 `RuntimeError`를 발생시킵니다.
- **의도치 않은 동작**: 검색 버튼이 나타나지 않거나, 검색 버튼을 클릭했는데도 불구하고 URL의 결과가 변경되지 않은 예외도 모두 `RuntimeError`로 빠른 실패를 유도합니다.

## 6. 스텝별 구현 맵 (Step-by-Step Implementation Map)
1. **리팩토링 파일 접근**: `src/gadget/skills/nobot/scripts/coupang_simulator.py` 파일 열기.
2. **함수 정의 수정**: 파일 하단 혹은 `run_search` 위/아래에 `_navigate_and_check`, `_perform_search`, `_verify_results` 3개의 비동기 함수 뼈대 선언 및 내부 로직 이동.
3. **오케스트레이터 수정**: 기존 `run_search` 함수의 `try` 블록 내부 로직들을 제거하고, 분할된 3개의 함수 호출 로직으로 교체.
4. **동작 확인 및 검증**: 수정 후 파이썬 문법 에러가 없는지, 시뮬레이터가 정상 동작하는지 테스트합니다 (`python src/gadget/skills/nobot/scripts/coupang_simulator.py`).
