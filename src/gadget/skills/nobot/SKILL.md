---
name: nobot
description: Human-like browser automation that bypasses bot detection using Real Chrome CDP.
version: 2.0.0
author: jujang
category: Automation / Browser
tags: [browser, bot-evasion, automation, human-like, cdp]
---

# Nobot — Human-like Browser Automation Skill

## Overview
Real Chrome을 CDP로 제어하여 봇 탐지(Akamai Bot Manager 등)를 우회하는 스킬.
Playwright bundled Chromium이 아닌 시스템 Chrome을 `--remote-debugging-port`로 실행하고 `connect_over_cdp()`로 연결하여 TLS/헤더 핑거프린트를 소비자 Chrome과 동일하게 유지한다.

## Architecture

```
ChromeLauncher (scripts/chrome_launcher.py)
    └─ Real Chrome subprocess (--remote-debugging-port, NO --enable-automation)
        └─ Playwright connect_over_cdp()
            └─ HumanoidInteractor (scripts/humanoid_interactor.py)
                ├─ Bezier mouse movement + jitter
                ├─ Human-like typing (down/up for ASCII, type for Korean/CJK)
                ├─ Burst scrolling
                └─ Warm-up (mouse move, hover, scroll, scroll-back)
```

## Scripts

스크립트는 이 스킬의 `scripts/` 폴더에 위치:

| File | Role |
|:---|:---|
| `scripts/chrome_launcher.py` | Real Chrome 실행 + CDP 연결 관리 |
| `scripts/humanoid_interactor.py` | 행동 레이어 (마우스, 키보드, 스크롤, warm-up) |
| `scripts/coupang_simulator.py` | 쿠팡 검색 시뮬레이터 (E2E 검증용) |

## Usage

### 쿠팡 검색 시뮬레이터 실행
```bash
python -u .agents/skills/nobot/scripts/coupang_simulator.py
```
"roborock" (영어) → "로보락" (한글) 순서로 검색 후 결과 검증.

### Python에서 직접 사용
```python
import asyncio, sys, os
# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".agents/skills/nobot/scripts"))

from playwright.async_api import async_playwright
from chrome_launcher import ChromeLauncher
from humanoid_interactor import HumanoidInteractor

async def search_coupang(query: str):
    launcher = ChromeLauncher()
    await launcher.start()

    async with async_playwright() as p:
        browser, page = await launcher.connect(p)
        interactor = HumanoidInteractor(page)

        await page.goto("https://www.coupang.com", wait_until="commit", timeout=60000)
        await asyncio.sleep(4)

        # Warm-up: feed Sensor Script with natural events
        await interactor.warm_up()

        # Type and search
        search_input = "#wa-search-form input.headerSearchKeyword"
        search_btn = "#wa-search-form button.headerSearchBtn"
        await page.wait_for_selector(search_input, state="visible", timeout=15000)
        await interactor.human_type(search_input, query)
        await asyncio.sleep(1)
        await interactor.human_click(search_btn)
        await asyncio.sleep(5)

        # Extract results (site-specific JS)
        results = await page.evaluate("""...""")

        await browser.close()
    await launcher.stop()
    return results
```

## Site Selectors (Coupang)

| Element | Selector |
|:---|:---|
| Search Input | `#wa-search-form input.headerSearchKeyword` |
| Search Button | `#wa-search-form button.headerSearchBtn` |
| Product Item | `li[class*="ProductUnit"]` |

## Key Principles

1. **Real Chrome First** — 핑거프린트를 코드로 해결하지 않음. 실제 Chrome이 요청 생성.
2. **No `--enable-automation`** — CDP 연결 시 자동화 플래그 제외. `navigator.webdriver = false`.
3. **Warm-Up Required** — 검색 전 반드시 마우스/스크롤 이벤트 생성 (Sensor Script 대응).
4. **Korean Input** — ASCII는 `keyboard.down/up`, 한글은 `keyboard.type()` 사용.

## Extending to Other Sites

새 사이트 추가 시:
1. 해당 사이트의 검색 input/button 셀렉터 파악
2. 결과 추출 JS 작성 (product item 셀렉터, 타이틀/가격/광고 추출)
3. `scripts/coupang_simulator.py`를 참고하여 새 시뮬레이터 작성
