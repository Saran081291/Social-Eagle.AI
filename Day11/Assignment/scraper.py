import asyncio
import os
from playwright.async_api import async_playwright

async def scrape_farmer_schemes():
    print("🌾 Starting Playwright scraper for Government Farmer Schemes...")
    
    # Path where the text file will be saved (Day11/Notes/)
    output_dir = os.path.join("..", "Notes")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "scraped_farmer_schemes.txt")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Target Government Portal (PM Kisan)
        url = "https://pmkisan.gov.in/"
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # Scrape text content from page
        portal_text = await page.inner_text("body")
        
        # Combine scraped content with detailed official scheme information
        knowledge_base = f"""
==================================================
OFFICIAL GOVERNMENT FARMER SCHEMES KNOWLEDGE BASE
Source: PM-Kisan Portal (https://pmkisan.gov.in)
==================================================

1. Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)
- Objective: Provide financial income support to all landholding farmer families across India.
- Benefits: Rs. 6,000 per year provided in three equal installments of Rs. 2,000 every 4 months directly to bank accounts via Direct Benefit Transfer (DBT).
- Eligibility: Landholding farmer families with cultivable land in their names.
- Exclusions: Institutional landholders, serving/retired government employees, income tax payers in the last assessment year, doctors, engineers, lawyers, and monthly pensioners above Rs. 10,000.
- Key Documents Required: Aadhaar card, bank account linked with Aadhaar, land ownership records (Khasra/Khatauni), mobile number.
- Registration Process: Online via PM-Kisan portal (Farmers Corner -> New Farmer Registration) or nearest Common Service Center (CSC).

2. Kisan Credit Card (KCC) Scheme
- Objective: Provide adequate and timely credit support to farmers for their agricultural needs at subsidized interest rates.
- Benefits: Short-term credit limit up to Rs. 3 Lakh at a concessional interest rate of 4% per annum (with 3% prompt repayment incentive).
- Eligibility: Farmers, tenant farmers, sharecroppers, and self-help groups (SHGs).

3. Pradhan Mantri Fasal Bima Yojana (PMFBY)
- Objective: Financial protection against crop loss due to natural calamities, pests, and diseases.
- Premium: 2% for Kharif crops, 1.5% for Rabi crops, and 5% for annual commercial/horticultural crops.
- Benefits: Comprehensive risk coverage from pre-sowing to post-harvest losses.

==================================================
Scraped Portal Content Summary:
{portal_text[:2000]}
"""
        # Save file in Day11/Notes/ folder
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(knowledge_base)
            
        print(f"✅ Data successfully scraped and saved to '{file_path}'!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_farmer_schemes())