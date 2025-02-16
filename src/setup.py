from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# Let webdriver-manager download the driver
chrome_driver_path = ChromeDriverManager().install()

# Check if webdriver-manager downloaded the WRONG file
if "THIRD_PARTY_NOTICES" in chrome_driver_path:
    print("⚠️ webdriver-manager downloaded an invalid file. Retrying...")
    os.remove(chrome_driver_path)  # Delete bad file
    chrome_driver_path = ChromeDriverManager().install()  # Try downloading again

# Ensure the driver is executable
os.chmod(chrome_driver_path, 0o755)

# Start Chrome WebDriver with the correct driver path
driver = webdriver.Chrome(service=Service(chrome_driver_path))

print("✅ ChromeDriver started successfully!")