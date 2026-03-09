# 기능 명세서: nobot 스킬

## 1. 개요 및 목적
`nobot` 스킬은 봇 탐지를 우회하고 실제 사람과 유사하게 브라우저를 제어하는 자동화 도구입니다. 웹 크롤링이나 E2E 테스트 과정에서 봇 차단을 우회해야 할 때 사용됩니다.

## 2. 사용법 (Trigger)
- **명령어**: `@nobot`

## 3. 주요 동작 방식 및 내부 로직
1. **Real Chrome CDP 연동**: 헤드리스(headless) 브라우저 대신 실제 Chrome 브라우저의 CDP(Chrome DevTools Protocol)를 사용하여 제어합니다.
2. **사람 모방 동작**: 마우스 이동 궤적, 스크롤 속도, 클릭 딜레이 등을 사람처럼 무작위화하여 봇 탐지 시스템(예: Cloudflare, reCAPTCHA 등)을 우회합니다.
3. **타겟 사이트 상호작용**: 스크립트(`scripts/chrome_launcher.py`, `scripts/humanoid_interactor.py` 등)를 통해 특정 웹사이트(예: Coupang 등)에 접근하고 자동화 작업을 수행합니다.

## 4. 제약 사항 및 예외 처리
- 실행 환경에 실제 Chrome 브라우저가 설치되어 있어야 합니다.
- 로컬 환경이나 GUI를 지원하는 CI/CD 환경에서만 정상 동작할 수 있습니다.
