# Research Report: `run_search` 함수 분리 분석

## 1. 개요
본 문서는 `src/gadget/skills/nobot/scripts/coupang_simulator.py` 파일 내에 정의된 `run_search` 함수가 단일 함수 50줄 제한(Simplicity 규칙)을 초과함에 따라, 이 함수의 책임을 분석하고 작은 단위의 함수로 분리하기 위한 분석 결과를 정리합니다.

## 2. 기존 `run_search` 함수의 문제점 및 책임 분석
현재 `run_search` 함수(약 60줄)는 브라우저 페이지 인스턴스를 생성하고, 페이지 내비게이션부터 최종 결과 검증까지 모든 동작을 순차적으로 처리하고 있어 책임이 과도하게 집중되어 있습니다.
주요 수행 동작을 6단계로 나눌 수 있습니다:
1. 내비게이션 (Navigation & Commit)
2. 센서 스크립트 대기 및 차단 여부 1차 확인 (Waiting for Sensor Script)
3. 웜업 (Warm-up)
4. 검색어 입력 (Type Query)
5. 검색 버튼 클릭 (Click Search)
6. 결과 대기 및 2차 검증 (Result Verification)

## 3. 분리 방안 및 아키텍처
`run_search`의 책임을 논리적인 단계로 나누어 각각 50줄 이내의 독립적인 비동기 함수로 분리하는 것이 적절합니다.

### 3.1 제안하는 함수 분할 설계
1. **`_navigate_and_check(page)`**
   - 역할: 설정된 URL("https://www.coupang.com")로 이동하고, 일정 시간 대기 후 페이지 타이틀을 통해 봇 차단 여부를 1차적으로 확인합니다.
   
2. **`_perform_search(page, interactor, query)`**
   - 역할: 우회 동작(warm-up)을 수행한 뒤, 검색 입력 폼을 찾고 `query`를 입력한 뒤 검색 버튼을 클릭합니다.
   
3. **`_verify_results(page, query)`**
   - 역할: 검색 수행 후 일정 시간 대기한 뒤, 페이지 URL 및 타이틀을 검증하여 검색 액션이 정상적으로 완료되었는지 파악하고 True 리턴 혹은 RuntimeError를 발생시킵니다.

4. **`run_search(query: str, launcher: ChromeLauncher)` (오케스트레이터)**
   - 역할: 브라우저와 페이지 환경을 설정하고, 위의 분리된 함수들을 순서대로 호출하는 역할만 수행합니다. 로직 흐름이 직관적으로 변해 가독성이 상승합니다.

## 4. 로직 변경 시나리오 (에지 케이스 및 유의사항)
- **에러 핸들링**: 기존 로직은 예외 상황에서 바로 `RuntimeError`를 발생(Fail-Fast) 시킵니다. 분할된 각 함수 내부에서도 이 패턴을 유지하여, 오류 발생 시 즉각적으로 오케스트레이터의 `try-except` 블록에서 잡아 처리되도록 합니다.
- **파라미터 전달**: 분할된 함수들은 `page` 객체와 필요에 따라 `interactor`, `query`를 매개변수로 명시적으로 전달받아야 합니다.

## 5. 결론
내부의 주요 기능들을 3개의 헬퍼 함수(`_navigate_and_check`, `_perform_search`, `_verify_results`)로 캡슐화하고 메인 `run_search`에서는 이를 호출만 하도록 변경함으로써 문제를 해결하고 길이를 50줄 미만으로 유지할 수 있습니다.
