import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import config
from login import login
from sbc import *
from store import *

# Generate timestamp for log filename
timestamp = time.strftime("%Y%m%d-%H%M%S")
log_filename = f'main_{timestamp}.log'

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
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_filename, filemode='w')

    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Call the login function
        login(driver)

        # Check for the presence of the live message and click the continue button if it exists
        check_and_click_continue(driver)

        # Flow Control - Step 1. SBC
        sbcs(driver)

        # Flow Control - Step 2. Open Packs
        open_packs(driver) 
    finally:
        # Close the browser when done
        driver.quit()

def sbcs(driver):
    # Solve daily challenges
    if config.SOLVE_DAILY_CHALLENGES:
        daily_challenges(driver)

    # Special SBC's
    if config.GOLD_UPGRADE:
        gold_upgrade(driver, 
                        repeats = config.GOLD_UPGRADE_COUNT, 
                        use_sbc_storage = config.GOLD_UPGRADE_USE_SBC_STORAGE)
    if config.SPECIAL_UPGRADE:
        special_upgrade(driver, config.SPECIAL_UPGRADE_NAME,
                                        repeats = config.SPECIAL_UPGRADE_COUNT, 
                                        use_sbc_storage = config.SPECIAL_UPGRADE_USE_SBC_STORAGE,
                                        rare_count = config.SPECIAL_UPGRADE_RARE_COUNT)
    if config.SPECIAL_CRAFTING_UPGRADE:
        # TODO: Put name in config
        special_crafting_upgrade(driver, "TOTS Crafting Upgrade", use_sbc_storage = config.SPECIAL_CRAFTING_UPGRADE_USE_SBC_STORAGE)

def open_packs(driver):
    # Open packs
    if config.OPEN_GOLD_PACKS:
        open_gold_packs(driver)
    if config.OPEN_CHEAP_PACKS:
        open_cheap_packs(driver)

if __name__ == "__main__":
    main()