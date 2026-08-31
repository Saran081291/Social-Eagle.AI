import re
from pathlib import Path

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.cricbuzz.com/", wait_until="domcontentloaded")

    eng_pak_scoreboard = page.get_by_text(
        re.compile(r"ENG\s+vs\s+PAK", re.IGNORECASE)
    ).first

    eng_pak_scoreboard.wait_for(state="visible")
    eng_pak_scoreboard.click()

    page.wait_for_timeout(3000)

    screenshot_path = Path(__file__).parent / "Criclivescore.png"
    page.screenshot(path=str(screenshot_path), full_page=True)

    print("Screenshot saved:", screenshot_path)

    browser.close()