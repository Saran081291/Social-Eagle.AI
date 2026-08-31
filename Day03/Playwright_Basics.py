from playwright.sync_api import sync_playwright
import pathlib 
from pathlib import Path

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.nseindia.com/market-data/live-equity-market")
    page.wait_for_load_state("networkidle")
    page.screenshot(path=pathlib.Path(__file__).parent / "nse_page.png")
    nifty50_price = page.locator("xpath=//div[@id='equityStockTable']/table/tbody/tr[1]/td[5]").inner_text()
    print("NIFTY 50 current price:", nifty50_price)
    browser.close()
