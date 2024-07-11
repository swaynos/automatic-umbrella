from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exceptions
import config
import os
import time

def take_screenshot(driver, error_message):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = os.path.join("screenshots", f"error_{timestamp}.png")
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
    driver.save_screenshot(screenshot_path)
    print(f"An error occurred: {error_message}. Screenshot saved to {screenshot_path}")

def wait_for_element(driver, by, value, timeout=config.DEFAULT_WAIT_DURATION):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def click_when_clickable(driver, by, value, timeout=config.DEFAULT_WAIT_DURATION):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    element.click()
    return element

def navigate_to_sbc(driver):
    # Wait for the navigation bar to be present
    wait_for_element(driver, By.CSS_SELECTOR, "nav.ut-tab-bar")
    # Click on the "SBC" button in the navigation bar
    click_when_clickable(driver, By.CSS_SELECTOR, "button.ut-tab-bar-item.icon-sbc")

def select_upgrades_menu(driver):
    # Wait for the menu to be visible
    wait_for_element(driver, By.CSS_SELECTOR, "div.menu-container")
    # Click on the "Upgrades" button in the menu
    click_when_clickable(driver, By.XPATH, "//button[contains(text(), 'Upgrades')]")

def open_daily_bronze_upgrade(driver):
    """
    Opens the Daily Bronze Upgrade page by scrolling down until the element is clickable and clicks on it.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        bool: True if the task is not complete, False if the task is complete.
    """
    # Wait for the page to load completely
    wait_for_element(driver, By.CSS_SELECTOR, "div.col-1-2-md.col-1-1.ut-sbc-set-tile-view")
    # Scroll down until the "Daily Bronze Upgrade" is visible and click it
    while True:
        try:
            daily_bronze_upgrade = driver.find_element(By.XPATH, "//h1[contains(text(), 'Daily Bronze Upgrade')]")
            parent_div = daily_bronze_upgrade.find_element(By.XPATH, "./ancestor::div[contains(@class, 'ut-sbc-set-tile-view')]")

            # Check if the parent div has the "complete" class
            if "complete" in parent_div.get_attribute("class"):
                print("Daily Bronze Upgrade is already complete.")
                return False  # Indicate that the task is complete

            daily_bronze_upgrade.click()
            break
        except selenium_exceptions.NoSuchElementException:
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(1)
    return True  # Indicate that the task is not complete

def use_squad_builder(driver):
    # Wait for the panel to be visible
    wait_for_element(driver, By.CSS_SELECTOR, "section.SquadPanel.SBCSquadPanel")
    # Click the "Use Squad Builder" button
    click_when_clickable(driver, By.XPATH, "//button[contains(text(), 'Use Squad Builder') and not(contains(@class, 'disabled'))]")

def set_sorting_and_quality(driver):
    time.sleep(1)  # Allow dropdown options to become visible
    # Change the sorting to "Lowest Quick Sell"
    click_when_clickable(driver, By.CSS_SELECTOR, "div.inline-list-select.ut-drop-down-control")
    click_when_clickable(driver, By.XPATH, "//li[contains(text(), 'Lowest Quick Sell')]")
    # Change the quality to "Bronze"
    quality_dropdown = click_when_clickable(driver, By.XPATH, "//div[contains(@class, 'ut-search-filter-control--row') and .//span[text()='Quality']]")
    bronze_option = click_when_clickable(driver, By.XPATH, "//li[contains(text(), 'Bronze')]")
    return quality_dropdown, bronze_option

def build_squad(driver):
    # Scroll down until the "Build" button is visible and click it
    build_button = wait_for_element(driver, By.XPATH, "//button[contains(text(), 'Build')]")
    build_button.click()
    print("'Build' button clicked successfully")

def check_sbc_requirements(driver):
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
        take_screenshot(driver, f"SBC requirements check failed: {str(e)}")
        raise  # Re-raise the exception to be handled by the caller

def submit_squad(driver):
    try:
        # Wait for the "Submit" button to be clickable
        submit_button = click_when_clickable(driver, By.XPATH, "//button[contains(@class, 'ut-squad-tab-button-control') and contains(@class, 'call-to-action') and contains(., 'Submit')]")
        print("'Submit' button clicked successfully")
    except Exception as e:
        take_screenshot(driver, f"Submit squad failed: {str(e)}")
        raise

def claim_rewards(driver):
    try:
        # Wait for the "Claim Rewards" button to be clickable
        claim_button = click_when_clickable(driver, By.XPATH, "//button[contains(@class, 'btn-standard') and contains(@class, 'call-to-action') and contains(text(), 'Claim Rewards')]")
        print("'Claim Rewards' button clicked successfully")
    except Exception as e:
        take_screenshot(driver, f"Claim rewards failed: {str(e)}")
        raise

def daily_challenges(driver):
    try:
        navigate_to_sbc(driver)
        select_upgrades_menu(driver)
        bronze_sbc_completable = open_daily_bronze_upgrade(driver)
        if bronze_sbc_completable:
            use_squad_builder(driver)
            set_sorting_and_quality(driver)
            build_squad(driver)
            check_sbc_requirements(driver)
            submit_squad(driver)
            claim_rewards(driver)
            claim_rewards(driver) # happens twice
    except selenium_exceptions.TimeoutException as e:
        take_screenshot(driver, "Timeout Exception occurred")
    except Exception as e:
        error_message = str(e)
        take_screenshot(driver, error_message)