import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import config
from login import login
from sbc import daily_challenges
from store import open_packs

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='main.log', filemode='w')

    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Call the login function
        login(driver)

        # Open packs
        open_packs(driver)

        # Solve daily challenges
        daily_challenges(driver)

    finally:
        # Close the browser when done
        driver.quit()

if __name__ == "__main__":
    main()