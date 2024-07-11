from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import config
from login import login
from sbc import daily_challenges

def main():
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Call the login function
        login(driver)

        daily_challenges(driver)

    finally:
        # Close the browser when done
        driver.quit()

if __name__ == "__main__":
    main()