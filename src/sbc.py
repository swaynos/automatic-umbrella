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

    # Locate the quality dropdown
    quality_dropdown = driver.find_element(By.XPATH, f"//div[contains(@class, 'ut-search-filter-control--row') and (.//span[text()='Quality'] or .//span[text()='{quality}'])]")
    
    # Scroll down to the quality dropdown to ensure it is in view, if necessary
    driver.execute_script("arguments[0].scrollIntoView(true);", quality_dropdown)
    
    # Click the quality dropdown
    quality_dropdown = click_when_clickable(driver, By.XPATH, f"//div[contains(@class, 'ut-search-filter-control--row') and (.//span[text()='Quality'] or .//span[text()='{quality}'])]")

    # Click the quality option
    quality_option = click_when_clickable(driver, By.XPATH, f"//div[contains(@class, 'ut-search-filter-control') and .//span[text()='Quality']]//ul/li[contains(text(), '{quality}')]")
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

def select_position(driver, position):
    """
    Selects a squad position based on the label, if the position is not locked.
    
    Args:
        driver: The Selenium WebDriver instance.
        position (str): The position label to select (e.g., "GK").
        
    Returns:
        bool: True if the position was successfully selected, else False.
    """
    # TODO: Is this try/catch block necessary? 
    try:
        # Wait for the panel to be visible
        wait_for_element(driver, By.CSS_SELECTOR, ".ut-squad-pitch-view.sbc")

        # Wait for the squad slots to be visible
        slots = driver.find_elements(By.CSS_SELECTOR, "div.ut-squad-slot-view:not(.locked)")

        for slot in slots:
            # Check for the position label within the slot
            label_element = slot.find_element(By.CSS_SELECTOR, "span.label")
            if label_element.text == position:
                slot.click()  # Click the slot to select the position
                logging.info(f"Selected position: {position}")
                return True  # Position selected successfully
        
        logging.warning(f"Position '{position}' not found or is locked.")
        return False  # Position not found or all are locked

    except selenium_exceptions.NoSuchElementException as e:
        logging.error(f"Could not find the position '{position}': {str(e)}")
        return False  # If any error occurs, return False

def click_add_player_button(driver):
    """
    Clicks the 'Add Player' button if it is visible and enabled.
    
    Args:
        driver: The Selenium WebDriver instance.
        
    Returns:
        bool: True if the button was successfully clicked, else False.
    """
    # Wait for the button to be visible and clickable
    add_player_button = driver.find_element(By.XPATH, "//button[span[@class='btn-text' and text()='Add Player']]")

    if add_player_button.is_displayed() and add_player_button.is_enabled():
        add_player_button.click()  # Click the button
        logging.info("Clicked 'Add Player' button successfully.")
        return True  # Button clicked successfully
    else:
        logging.warning("Add Player button is not displayed or enabled.")
        return False  # Button is not clickable

def close_active_filter_by_position(driver, position):
    """
    Clicks the (close) button within the active element if it is visible and enabled.
    
    Args:
        driver: The Selenium WebDriver instance.
        position (str): The position label to look for (e.g., "GK").
        
    Returns:
        bool: True if the button was successfully clicked, else False.
    """
    # Locate the active element that contains the desired position
    active_elements = driver.find_elements(By.CSS_SELECTOR, "div.has-selection")
    
    for active_element in active_elements:
        # Find the span with the position text
        position_label = active_element.find_element(By.CSS_SELECTOR, "span.label")
        if position_label.text.strip() == position:
            # Locate the button within the matching active element
            button = active_element.find_element(By.CSS_SELECTOR, "button.flat.ut-search-filter-control--row-button")
            
            if button.is_displayed() and button.is_enabled():
                button.click()  # Click the button
                logging.info(f"Clicked the button for position '{position}' successfully.")
                return True  # Button clicked successfully

    logging.warning(f"No active element found with position '{position}' or button is not clickable.")
    return False  # No matching active element or button is not enabled/clickable

def click_search_button(driver):
    # Wait until the "Search" button is clickable and perform the click
    search_button = click_when_clickable(driver, By.XPATH, "//button[contains(@class, 'btn-standard') and contains(@class, 'call-to-action') and text()='Search']")
    logging.info("Clicked on the 'Search' button successfully.")
    return search_button  # Return the clicked button if needed

def click_first_add_player(driver):
    # Construct the XPath to find the first "add" button
    add_button_xpath = "//li//button[contains(@class, 'add')]"
    
    # Use the existing click_when_clickable utility function
    add_button = click_when_clickable(driver, By.XPATH, add_button_xpath)
    
    logging.info("Clicked the first available 'Add' button.")
    return add_button  # Return the button or perform further actions as needed


def daily_simple_upgrade(driver, challenge_name, sort_type, quality, position="GK", size = 3):
    """
    Completes a daily simple upgrade challenge that requires only one position of specified quality.

    Args:
        driver: The Selenium WebDriver instance used to interact with the web application.
        challenge_name (str): The name of the simple upgrade challenge to complete.
        sort_type (str): The sorting type to be applied when using the squad builder (e.g., "Lowest Quick Sell").
        quality (str): The quality level of the position required for the challenge (e.g., "Bronze").
        size (int): The number of times the upgrade challenge will be attempted. Defaults to 3.

    This function performs the following steps:
    1. Navigates to the Squad Building Challenges (SBC) section.
    2. Selects the upgrades menu.
    3. For the specified number of attempts (size):
        - Opens the daily upgrade associated with challenge_name.
        - If the upgrade is completable, proceeds to use the squad builder.
        - Sets the sorting and quality for the squad builder based on the provided parameters.
        - Builds the squad and checks for SBC requirements.
        - Submits the squad and claims rewards. This process is repeated twice for the claimRewards step.

    Note:
        Each successful completion of the challenge awards rewards, which are claimed after each submission.
    """
    navigate_to_sbc(driver)
    select_upgrades_menu(driver)
    for i in range(size):
        sbc_completable = open_daily_upgrade(driver, challenge_name)
        if sbc_completable:
            time.sleep(1)
            if (select_position(driver, position)):
                click_add_player_button(driver)
                time.sleep(.5)  # Allow dropdown options to become visible
                set_sorting_and_quality(driver, sort_type, quality)
                close_active_filter_by_position(driver, position)
                click_search_button(driver)
                time.sleep(1)
                click_first_add_player(driver)
                time.sleep(.5)
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
        daily_simple_upgrade(driver, "FUTTIES Daily Login Upgrade", sort_type, "Bronze", "GK", 1)
        daily_gold_upgrade(driver, sort_type)
    except selenium_exceptions.TimeoutException as e:
        take_screenshot(driver)
        logging.error(f"Timeout Exception occurred: {str(e)}")
    except Exception as e:
        error_message = str(e)
        take_screenshot(driver)
        logging.error(f"An error occurred: {error_message}")
    # TODO: Consider retrying on exception
    