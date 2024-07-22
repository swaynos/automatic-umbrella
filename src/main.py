import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import config
from login import login
from sbc import daily_challenges
from store import open_packs

def check_and_click_continue(driver):
    """Check if the live message is present and click the continue button if it is."""
    try:
        # Wait for the live message element to be present with a timeout
        WebDriverWait(driver, config.DEFAULT_WAIT_DURATION).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ut-livemessage"))
        )

        # If we reach here, it means the live message is present
        logging.info("Live message detected. Attempting to click the continue button.")
        
        # Find the live message container
        message_element = driver.find_element(By.CLASS_NAME, "ut-livemessage")
        continue_button = message_element.find_element(By.CLASS_NAME, "btn-standard.call-to-action")

        # Click the continue button
        continue_button.click()
        logging.info("Continue button clicked successfully.")

    except Exception as e:
        # Log the exception and proceed without interruption
        logging.info("No live message detected, or an error occurred: %s", str(e))

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='main.log', filemode='w')

    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Call the login function
        login(driver)

        # Check for the presence of the live message and click the continue button if it exists
        check_and_click_continue(driver)

        # Open packs
        open_packs(driver)

        # Solve daily challenges
        daily_challenges(driver)

    finally:
        # Close the browser when done
        driver.quit()

if __name__ == "__main__":
    main()