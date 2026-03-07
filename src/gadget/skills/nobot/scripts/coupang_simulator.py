"""
Coupang Bot Bypass Simulator — v5

Uses REAL Chrome via CDP (no bundled Chromium).
TLS/header fingerprints are identical to consumer Chrome.

Flow:
  1. Launch Real Chrome with --remote-debugging-port (no --enable-automation)
  2. Connect via Playwright connect_over_cdp()
  3. Navigate to Coupang → warm_up → type → search → verify
"""
import asyncio
import random
import sys
import os

# Allow running from the scripts directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.async_api import async_playwright
from chrome_launcher import ChromeLauncher
from humanoid_interactor import HumanoidInteractor

SEARCH_INPUT = "#wa-search-form input.headerSearchKeyword"
SEARCH_BTN = "#wa-search-form button.headerSearchBtn"


async def run_search(query: str, launcher: ChromeLauncher) -> bool:
    async with async_playwright() as p:
        browser, page = await launcher.connect(p)
        interactor = HumanoidInteractor(page)

        try:
            # 1. Navigate (use 'commit' for fastest response)
            print(f"[*] Navigating to Coupang…")
            await page.goto(
                "https://www.coupang.com",
                wait_until="commit",
                timeout=60000,
            )
            print("[*] Page committed.")

            # 2. Wait for Sensor Script
            wait_s = random.uniform(3, 5)
            print(f"[*] Waiting {wait_s:.1f}s for Sensor Script…")
            await asyncio.sleep(wait_s)

            title = await page.title()
            print(f"[*] Page title: {title}")
            if _is_blocked(title):
                raise RuntimeError("Immediate Access Denied.")

            # 3. Warm-up
            print("[*] Running warm-up…")
            await interactor.warm_up()

            # 4. Type query — wait for search input to be visible first
            print(f"[*] Waiting for search input…")
            await page.wait_for_selector(SEARCH_INPUT, state="visible", timeout=15000)
            print(f"[*] Typing: {query}")
            await interactor.human_type(SEARCH_INPUT, query)

            # 5. Click search
            await asyncio.sleep(random.uniform(0.5, 1.5))
            print("[*] Clicking search…")
            await interactor.human_click(SEARCH_BTN)

            # 6. Wait for results (simple sleep — more reliable than load_state for SPAs)
            print("[*] Waiting for results…")
            await asyncio.sleep(5)

            final_url = page.url
            final_title = await page.title()
            print(f"[*] Result URL: {final_url}")
            print(f"[*] Result title: {final_title}")
            if _is_blocked(final_title):
                raise RuntimeError(f"Access Denied after search for '{query}'.")

            if "search" in final_url or query.lower() in final_url.lower():
                print(f"[+] SUCCESS: '{query}' results loaded.")
                return True

            raise RuntimeError(f"Search failed: URL unchanged after clicking search. Result URL: {final_url}")

        except Exception as e:
            print(f"[!] Error: {e}")
            raise RuntimeError(f"Unexpected error: {e}") from e


def _is_blocked(title: str) -> bool:
    return "access denied" in title.lower()


async def main():
    print("=== Coupang Bot Bypass Simulator v5 ===")
    print("    (Real Chrome via CDP)\n")

    launcher = ChromeLauncher()
    await launcher.start()

    try:
        # Test 1: English
        print("--- Test 1: English Search (roborock) ---")
        if not await run_search("roborock", launcher):
            print("[!] English test failed. Aborting (IP protection).")
            sys.exit(1)

        await asyncio.sleep(2)

        # Test 2: Korean
        print("\n--- Test 2: Korean Search (로보락) ---")
        if not await run_search("로보락", launcher):
            print("[!] Korean test failed.")
            sys.exit(1)

        print("\n[***] ALL TESTS PASSED [***]")
    finally:
        await launcher.stop()


if __name__ == "__main__":
    asyncio.run(main())
