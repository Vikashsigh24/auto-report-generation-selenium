
import os
import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set download directory
download_dir = os.path.abspath("downloads")
os.makedirs(download_dir, exist_ok=True)

# Configure Chrome options for auto PDF download
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "plugins.always_open_pdf_externally": True,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
})
chrome_options.add_argument("--start-maximized")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # STEP 1: Open the assessment/report page
    driver.get("https://assessment.careerguide.com/Assessment/Reports/pdf/eg-l2/326312.pdf")

    # STEP 2: Click the "Get Report" button dynamically (adjust selector as needed)
    get_report_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Get Report')]"))
    )
    get_report_btn.click()

    # STEP 3: Wait until a PDF URL is loaded
    WebDriverWait(driver, 30).until(
        EC.url_contains(".pdf")
    )

    # STEP 4: Get PDF URL dynamically from current tab
    pdf_url = driver.current_url
    print(f"PDF URL Detected: {pdf_url}")

    # STEP 5: Create dynamic filename using current date-time
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Engineering_Report_{now}.pdf"
    filepath = os.path.join(download_dir, filename)

    # STEP 6: Download PDF using requests (you can also let Chrome download automatically)
    response = requests.get(pdf_url)
    with open(filepath, "wb") as file:
        file.write(response.content)
    
    print(f"✅ Report downloaded: {filepath}")

finally:
    time.sleep(3)
    driver.quit()
