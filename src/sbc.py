import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exceptions
import config
import time

from utilities import take_screenshot, wait_for_element, click_when_clickable

def navigate_to_sbc(driver):
    # Wait for the navigation bar to be present
    wait_for_element(driver, By.CSS_SELECTOR, "nav.ut-tab-bar")
    # Click on the "SBC" button in the navigation bar
    click_when_clickable(driver, By.CSS_SELECTOR, "button.ut-tab-bar-item.icon-sbc")
    logging.info("Navigated to the sbc page.")

def select_upgrades_menu(driver):
    # Wait for the menu to be visible
    wait_for_element(driver, By.CSS_SELECTOR, "div.menu-container")
    # Click on the "Upgrades" button in the menu
    click_when_clickable(driver, By.XPATH, "//button[contains(text(), 'Upgrades')]")
    logging.info("Clicked on the Upgrades menu.")

def open_daily_upgrade(driver, upgrade_name = "Daily Bronze Upgrade"):
    """
    Opens the SBC Upgrade page by scrolling down until the element is clickable and clicks on it.

    Args:
        driver: The Selenium WebDriver instance.
        upgrade_name (str): The name of the upgrade to open. Defaults to "Daily Bronze Upgrade".

    Returns:
        int: The repeatable count associated with the sbc.

    This function waits for the page to load completely before scrolling down to find the specified upgrade by name.
    It checks if the upgrade is already marked as complete and returns False in that case.
    If the upgrade is not complete, it clicks on the upgrade and retrieves the repeatable count associated with it.
    The repeatable count is returned to indicate the number of times the task can be repeated.
    """
    # Wait for the page to load completely
    wait_for_element(driver, By.CSS_SELECTOR, "div.col-1-2-md.col-1-1.ut-sbc-set-tile-view")

    # Scroll down until the "Daily Bronze Upgrade" is visible and click it
    while True:
        try:
            upgrade_header = driver.find_element(By.XPATH, f"//h1[contains(text(), '{upgrade_name}')]")
            parent_div = upgrade_header.find_element(By.XPATH, "./ancestor::div[contains(@class, 'ut-sbc-set-tile-view')]")

            # Check if the parent div has the "complete" class
            if "complete" in parent_div.get_attribute("class"):
                print(f"{upgrade_name} is already complete.")
                return 0  # Indicate that the task is complete with 0 repeatable count

            # Click the upgrade header
            upgrade_header.click()

            # Extract the repeatable count
            repeatable_element = parent_div.find_element(By.CSS_SELECTOR, "div.ut-squad-building-set-status-label-view.repeat span.text")
            repeatable_text = repeatable_element.text
            repeatable_count = int(repeatable_text.split(" ")[1])
            return repeatable_count  # Return the repeatable count
        except selenium_exceptions.NoSuchElementException:
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(1)

def use_squad_builder(driver):
    # Wait for the panel to be visible
    wait_for_element(driver, By.CSS_SELECTOR, "section.SquadPanel.SBCSquadPanel")
    # Click the "Use Squad Builder" button
    click_when_clickable(driver, By.XPATH, "//button[contains(text(), 'Use Squad Builder') and not(contains(@class, 'disabled'))]")
    logging.info("Clicked on the 'Use Squad Builder' button.")

def set_sorting_and_quality(driver, sort = "Lowest Quick Sell", quality = "Bronze"):
    # Change the sorting to "Lowest Quick Sell"
    click_when_clickable(driver, By.CSS_SELECTOR, "div.inline-list-select.ut-drop-down-control")
    click_when_clickable(driver, By.XPATH, f"//li[contains(text(), '{sort}')]")
    # Change the quality to quality
    quality_dropdown = click_when_clickable(driver, By.XPATH, f"//div[contains(@class, 'ut-search-filter-control--row') and (.//span[text()='Quality'] or .//span[text()='{quality}'])]")
    quality_option = click_when_clickable(driver, By.XPATH, f"//li[contains(text(), '{quality}')]")
    logging.info(f"Set sorting to '{sort}' and quality to '{quality}'.")
    return quality_dropdown, quality_option

def build_squad(driver):
    # Scroll down until the "Build" button is visible and click it
    build_button = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'Build')]")
    build_button.click()
    logging.info("Clicked on the 'Build' button.")

def select_challenge(driver, challenge_name):
    """
    Selects a specific challenge by finding the corresponding element based on the provided challenge name.
    
    Args:
        driver: The Selenium WebDriver instance.
        challenge_name (str): The name of the challenge to select.
        
    Returns:
        bool: True if the challenge is not complete and successfully selected, False if the challenge is already complete.
    """
    # Wait for the challenge row to be present
    challenge_row = wait_for_element(driver, By.XPATH, f"//h1[contains(text(), '{challenge_name}')]/ancestor::div[contains(@class, 'ut-sbc-challenge-table-row-view')]")

    # Check if the challenge is already completed
    if "complete" in challenge_row.get_attribute("class"):
        logging.warning(f"'{challenge_name}' is already complete.")
        return False

    # Click the challenge row
    challenge_row.click()
    logging.info(f"'{challenge_name}' selected successfully")
    return True

def start_challenge(driver):
    # Wait for either "Start Challenge" or "Go to Challenge" button to be clickable and click it
    start_button = WebDriverWait(driver, config.DEFAULT_WAIT_DURATION).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'btn-standard') and contains(@class, 'call-to-action') and (contains(text(), 'Start Challenge') or contains(text(), 'Go to Challenge'))]")
        )
    )
    start_button.click()
    logging.info("Clicked on the 'Start Challenge' or 'Go to Challenge' button.")

def check_sbc_requirements(driver):
    # TODO: Is this try/catch block necessary?
    try:
        # Wait for the requirements checklist to be present
        requirements_list = wait_for_element(driver, By.CSS_SELECTOR, "ul.sbc-requirements-checklist")

        # Get all list items within the requirements checklist
        list_items = requirements_list.find_elements(By.TAG_NAME, "li")

        # Check if all list items have the class "complete"
        for item in list_items:
            if "complete" not in item.get_attribute("class"):
                raise Exception(f"Requirement not complete: {item.text}")

        print("All SBC requirements are complete.")
    except Exception as e:
        take_screenshot(driver)
        logging.error(f"SBC requirements check failed: {str(e)}")
        raise  # Re-raise the exception to be handled by the caller

def submit_squad(driver):
    # Wait for the "Submit" button to be clickable
    click_when_clickable(driver, By.XPATH, "//button[contains(@class, 'ut-squad-tab-button-control') and contains(@class, 'call-to-action') and contains(., 'Submit')]")
    logging.info("Clicked on the 'Submit' button.")

def claim_rewards(driver):
    # Wait for the "Claim Rewards" button to be clickable
    claim_button = click_when_clickable(driver, By.XPATH, "//button[contains(@class, 'btn-standard') and contains(@class, 'call-to-action') and contains(text(), 'Claim Rewards')]")
    logging.info(f"Clicked on the 'Claim Rewards' button.")

def daily_simple_upgrade(driver, challenge_name, sort_type, quality):
    navigate_to_sbc(driver)
    select_upgrades_menu(driver)
    for i in range(3):
        sbc_completable = open_daily_upgrade(driver, challenge_name)
        if sbc_completable:
            use_squad_builder(driver)
            time.sleep(1)  # Allow dropdown options to become visible
            set_sorting_and_quality(driver, sort_type, quality)
            time.sleep(.5)
            build_squad(driver)
            time.sleep(1)
            check_sbc_requirements(driver)
            submit_squad(driver)
            claim_rewards(driver)
            claim_rewards(driver) # happens twice
            i += 1

def daily_gold_upgrade(driver, sort_type):
    navigate_to_sbc(driver)
    select_upgrades_menu(driver)
    sbc_completable = open_daily_upgrade(driver, "Daily Gold Upgrade")
    if sbc_completable > 0:
        for i in range(sbc_completable):
            time.sleep(1) # Allow the SBC an opportunity to load
            if select_challenge(driver, "Bronze Challenge"):
                start_challenge(driver)
                use_squad_builder(driver)
                time.sleep(1)  # Allow dropdown options to become visible
                set_sorting_and_quality(driver, sort_type, "Bronze")
                time.sleep(.5)
                build_squad(driver)
                time.sleep(2) # Allow requirements to update
                check_sbc_requirements(driver)
                submit_squad(driver)
                claim_rewards(driver)

            if select_challenge(driver, "Silver Challenge"):
                start_challenge(driver)
                use_squad_builder(driver)
                time.sleep(1)  # Allow dropdown options to become visible
                set_sorting_and_quality(driver, sort_type, "Silver")
                time.sleep(.5)
                build_squad(driver)
                time.sleep(2) # Allow requirements to update
                check_sbc_requirements(driver)
                submit_squad(driver)
                claim_rewards(driver)

            claim_rewards(driver) # The 3rd claim rewards button is for the Gold upgrade
            i += 1

def daily_challenges(driver: webdriver):
    try:
        sort_type = "Lowest Quick Sell"
        daily_simple_upgrade(driver, "Daily Bronze Upgrade", sort_type, "Bronze")
        daily_simple_upgrade(driver, "Daily Silver Upgrade", sort_type, "Silver")
        daily_gold_upgrade(driver, sort_type)
    except selenium_exceptions.TimeoutException as e:
        take_screenshot(driver)
        logging.error(f"Timeout Exception occurred: {str(e)}")
    except Exception as e:
        error_message = str(e)
        take_screenshot(driver)
        logging.error(f"An error occurred: {error_message}")
    # TODO: Consider retrying on exception
    