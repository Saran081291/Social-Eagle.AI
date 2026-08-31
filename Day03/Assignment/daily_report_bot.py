import time
from datetime import datetime
from pathlib import Path

import pyautogui
import pyperclip


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1

# Open Chrome and select the Saran Jebaraj profile
print("Opening Chrome browser...")
pyautogui.hotkey("win", "r")
time.sleep(1)
pyautogui.write("chrome", interval=0.1)
pyautogui.press("enter")

time.sleep(5)
pyautogui.click(510, 470)  # Saran Jebaraj Chrome profile

# Open NSE and copy the NIFTY 50 current price
pyautogui.hotkey("ctrl", "t")
time.sleep(1)

pyperclip.copy("https://www.nseindia.com")
pyautogui.hotkey("ctrl", "v")
pyautogui.press("enter")

time.sleep(6)
pyautogui.doubleClick(230, 558, interval=0.15)
time.sleep(0.5)

pyautogui.hotkey("ctrl", "c")
time.sleep(0.5)

nifty50_price = pyperclip.paste().strip()

print("NIFTY 50 current price:", nifty50_price)

# Open Excel and create a blank workbook
print("Opening Microsoft Excel...")
pyautogui.hotkey("win", "r")
time.sleep(1)
pyautogui.write("excel", interval=0.1)
pyautogui.press("enter")

time.sleep(8)
pyautogui.press("enter")
time.sleep(8)

# Add one row: date/time, NIFTY 50 price, comment
date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
comment = "NIFTY 50 is being tracked for today's report."

row = f"{date_time}\t{nifty50_price}\t{comment}"

pyautogui.hotkey("ctrl", "home")
pyperclip.copy(row)
pyautogui.hotkey("ctrl", "v")
pyautogui.press("enter")

pyautogui.hotkey("ctrl", "home")
time.sleep(1)

pyautogui.hotkey("ctrl", "a")
time.sleep(1)

pyautogui.hotkey("alt", "h")
time.sleep(0.5)

pyautogui.press("o")
time.sleep(0.5)

pyautogui.press("i")  # AutoFit Column Width
time.sleep(3)

today = datetime.now().strftime("%Y-%m-%d")
project_folder = Path(__file__).resolve().parent
excel_path = project_folder / f"daily_report_{today}.xlsx"

if excel_path.exists():
    raise FileExistsError(f"File already exists: {excel_path}")

pyautogui.press("f12")  # Save As
time.sleep(3)

pyperclip.copy(str(excel_path))
pyautogui.hotkey("ctrl", "a")
pyautogui.hotkey("ctrl", "v")
pyautogui.press("enter")
time.sleep(5)

# Maximize Excel, then capture the final sheet
pyautogui.hotkey("alt", "space")
pyautogui.press("x")
time.sleep(2)

screenshot_path = project_folder / f"daily_report_{today}.png"
pyautogui.screenshot(str(screenshot_path))

print("Excel file saved:", excel_path)
print("Final Excel screenshot saved:", screenshot_path)