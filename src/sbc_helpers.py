import logging

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exceptions
import config
import time

from utilities import *

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

    upgrade_header = find_sbc(driver, upgrade_name)
    
    if upgrade_header is None:
        return 0
    
    parent_div = upgrade_header.find_element(By.XPATH, "./ancestor::div[contains(@class, 'ut-sbc-set-tile-view')]")

    # Check if the parent div has the "complete" class
    if "complete" in parent_div.get_attribute("class"):
        logging.info(f"{upgrade_name} is already complete.")
        return 0  # Indicate that the task is complete with 0 repeatable count

    # Extract the repeatable count
    repeatable_element = parent_div.find_element(By.CSS_SELECTOR, "div.ut-squad-building-set-status-label-view.repeat span.text")
    repeatable_text = repeatable_element.text
    try:
        # If it's infinately repeatable, this will throw an error
        repeatable_count = int(repeatable_text.split(" ")[1])
    except:
        repeatable_count = -1
    logging.info(f"Repeatable count for {upgrade_name}: {repeatable_count}")

    if repeatable_count == 0:  
        return 0

    # Click the upgrade header
    upgrade_header.click()
    logging.info(f"Clicked the {upgrade_name} upgrade.")

    return repeatable_count  # Return the repeatable count

def find_sbc(driver, sbc_name, max_scroll_attempts=10):
    try:
        parent_div = wait_for_element(driver, By.CSS_SELECTOR, "div.ut-navigation-container-view--content .container")
        scroll_attempts = 0

        while scroll_attempts < max_scroll_attempts:
            try:
                sbc_element = parent_div.find_element(By.XPATH, f"//h1[@class='tileTitle' and contains(text(), '{sbc_name}')]")
                logging.info(f"Found sbc: {sbc_name}")
                return sbc_element
            except selenium_exceptions.NoSuchElementException:
                driver.execute_script("arguments[0].scrollBy(0, 150);", parent_div)
                time.sleep(0.1) # You want to throttle this so that you don't scroll too fast.
                # I'm not sure if there is something to wait for instead of just sleeping.
                scroll_attempts += 1

        print(f"Reached max scroll attempts. Could not find pack: {sbc_name}")
        return None
    except Exception as e:
        print(f"Could not find pack: {sbc_name}. Error: {str(e)}")
        return None

def use_squad_builder(driver):
    # Wait for the panel to be visible
    wait_for_element(driver, By.CSS_SELECTOR, "section.SquadPanel.SBCSquadPanel")
    # Click the "Use Squad Builder" button
    click_when_clickable(driver, By.XPATH, "//button[contains(text(), 'Use Squad Builder') and not(contains(@class, 'disabled'))]")
    logging.info("Clicked on the 'Use Squad Builder' button.")

def set_rarity(driver, rarity = "Common"):
    click_when_clickable(
        driver,
        By.XPATH,
        "//div[contains(@class, 'ut-search-filter-control--row') and (.//span[text()='Rarity'] or .//span[text()='Rare'] or .//span[text()='Common'])]"
    )
    logging.info("Clicked on 'Rarity' filter.")
    click_when_clickable(
        driver,
        By.XPATH,
        f"//li[contains(@class, 'with-icon') and text()='{rarity}']"
    )
    logging.info(f"Clicked on '{rarity}'.")

def set_sorting_and_quality(driver, sort = "Lowest Quick Sell", quality = "Bronze"):
    # Change the sorting to "Lowest Quick Sell"
    # Make sure the selector is in view
    sort_by_selector = "div.inline-list-select.ut-drop-down-control"
    sort_by = driver.find_element(By.CSS_SELECTOR, sort_by_selector)
    driver.execute_script("arguments[0].scrollIntoView(true);", sort_by)
    # Click the selector
    sort_by.click()
    # Select the sort type
    click_when_clickable(driver, By.XPATH, f"//li[contains(text(), '{sort}')]")
    logging.info(f"Set sorting to '{sort}'.")

    # Locate the quality dropdown
    quality_selector = f"//div[contains(@class, 'ut-search-filter-control--row') and (.//span[text()='Quality'] or .//span[text()='Bronze'] or .//span[text()='Silver'] or .//span[text()='Gold'])]"
    quality_dropdown = driver.find_element(By.XPATH, quality_selector)
    
    # Scroll down to the quality dropdown to ensure it is in view, if necessary
    driver.execute_script("arguments[0].scrollIntoView(true);", quality_dropdown)
    logging.info(f"Scrolled until the quality filter is in view.")
    
    # Click the quality dropdown
    quality_dropdown.click()
    logging.info(f"Clicked on the quality filter.")

    # Get the sibling elements
    siblings = quality_dropdown.get_attribute("innerHTML")
   
    # Check if any `ul` siblings exist
    if siblings:
        quality_option = click_when_clickable(driver, By.XPATH, f"//div[contains(@class, 'inline-list-select')]//ul[@class='inline-list']/li[contains(text(), '{quality}')]")
        logging.info(f"Clicked on the quality option '{quality}'.")
    else:
        # TODO: I'm not sure if this is ever hit
        # Click the quality dropdown        
        click_when_clickable(driver, By.XPATH, f"//div[contains(@class, 'ut-search-filter-control--row') and (.//span[text()='Quality'] or .//span[text()='{quality}'])]")
        logging.info(f"Clicked on the quality filter.")

        # Click the quality option
        quality_option = click_when_clickable(driver, By.XPATH, f"//div[contains(@class, 'ut-search-filter-control') and .//span[text()='Quality']//ul/li[contains(text(), '{quality}')]")
        logging.info(f"Clicked on the quality option '{quality}'.")

    logging.info(f"Completed sorting to '{sort}' and quality to '{quality}'.")
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

def sbc_requirements_popover_visible(driver):
    # Locate the element (adjust the selector as needed)
    element = driver.find_element(By.CSS_SELECTOR, "div.ut-popover")

    # Get the class attribute and split it into individual class names
    classes = element.get_attribute("class").split()

    # Check if 'show' is in the list of classes
    if "show" in classes:
        logging.info("SBC Requirements popover has the 'show' class.")
        return True
    else:
        logging.info("SBC Requirements popover does not have the 'show' class.")
        return False

# Returns bool indicating the validity of the squad
def check_sbc_requirements(driver):
    squad_valid = False

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
        squad_valid = True
    except Exception as e:
        logging.error(f"SBC requirements check failed: {str(e)}")
        squad_valid = False

    return squad_valid

def submit_squad(driver):
    # Wait for the "Submit" button to be clickable
    click_when_clickable(driver, By.XPATH, "//button[contains(@class, 'ut-squad-tab-button-control') and contains(@class, 'call-to-action') and contains(., 'Submit')]")
    logging.info("Clicked on the 'Submit' button.")

def claim_rewards(driver):
    # Wait for the "Claim Rewards" button to be clickable
    claim_button = click_when_clickable(driver, By.XPATH, "//button[contains(@class, 'btn-standard') and contains(@class, 'call-to-action') and contains(text(), 'Claim Rewards')]")
    logging.info(f"Clicked on the 'Claim Rewards' button.")

def select_position(driver, position="", index=-1):
    """
    Selects a squad slot based on either the provided index attribute or the position label.
    
    Args:
        driver: The Selenium WebDriver instance.
        position (str, optional): The position label to select (e.g., "GK"). Defaults to "".
        index (int, optional): The index of the slot to select. If >= 0, this is used instead of the position. Defaults to -1.
        
    Returns:
        str: The position label (e.g., "GK", "ST") from the selected slot if successful, else None.
    """
    try:
        # Wait for the pitch view to be visible
        wait_for_element(driver, By.CSS_SELECTOR, ".ut-squad-pitch-view.sbc")
        
        selected_slot = None
        if index >= 0:
            # Select slot using its index attribute
            slot_selector = f"div.ut-squad-slot-view[index='{index}']"
            selected_slot = driver.find_element(By.CSS_SELECTOR, slot_selector)
            logging.info(f"Selecting slot with index: {index}")
        else:
            # Find all squad slots that are not locked
            slots = driver.find_elements(By.CSS_SELECTOR, "div.ut-squad-slot-view:not(.locked)")
            for s in slots:
                label_element = s.find_element(By.CSS_SELECTOR, "span.label")
                if label_element.text.strip() == position:
                    selected_slot = s
                    logging.info(f"Selecting slot with position: {position}")
                    break
            if selected_slot is None:
                logging.warning(f"Position '{position}' not found or is locked.")
                return None

        # Extract the position label from the selected slot
        label_element = selected_slot.find_element(By.CSS_SELECTOR, "span.label")
        slot_position = label_element.text.strip()

        # Hover over the slot and click it
        actions = ActionChains(driver)
        actions.move_to_element(selected_slot).perform()
        selected_slot.click()

        return slot_position

    except selenium_exceptions.NoSuchElementException as e:
        logging.error(f"Error selecting slot (position='{position}', index={index}): {str(e)}")
        return None

def is_slot_filled(driver, index):
    """
    Checks if the squad slot at the given index is filled by looking for a child div with class "playerOverview"
    and its child <div class="rating"></div>. If the rating's text is not empty, then the slot is considered filled.
    
    Args:
        driver: The Selenium WebDriver instance.
        index (int): The index of the slot to check.
        
    Returns:
        bool: True if the slot is filled (rating is not empty), False otherwise.
    """
    try:
        # Locate the slot by its index attribute.
        slot_selector = f"div.ut-squad-slot-view[index='{index}']"
        slot = driver.find_element(By.CSS_SELECTOR, slot_selector)
        
        # Look for the rating element under the playerOverview div.
        rating_element = slot.find_element(By.CSS_SELECTOR, "div.playerOverview div.rating")
        rating_text = rating_element.get_attribute("textContent").strip()
        
        if rating_text:
            logging.info(f"Slot {index} is filled with rating: {rating_text}")
            return True
        else:
            logging.info(f"Slot {index} rating is empty, so it is not filled.")
            return False

    except Exception as e:
        logging.error(f"Error checking if slot {index} is filled: {str(e)}")
        return False

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


def toggle_ignore_position(driver):
    # Construct the XPath to find the "Ignore Position" toggle
    ignore_position_xpath = "//span[contains(text(), 'Ignore Position')]/../div[contains(@class, 'ut-toggle-control')]/div[contains(@class, 'ut-toggle-control--track')]"

    toggle = driver.find_element(By.XPATH, ignore_position_xpath)

    if toggle.is_displayed() and toggle.is_enabled():
        toggle.click()  # Click the button
        logging.info("Clicked 'Ignore Position' toggle successfully.")
        return True  # clicked successfully
    else:
        logging.warning("Ignore Position toggle is not displayed or enabled.")
        return False  # is not clickable

def set_sbc_storage(driver):
    click_when_clickable(
        driver,
        By.XPATH,
        "//div[contains(@class, 'ut-search-filter-control--row') and .//span[text()='My Club']]"
    )
    logging.info("Clicked on 'My Club' filter.")
    click_when_clickable(
        driver,
        By.XPATH,
        "//li[contains(@class, 'with-icon') and text()='SBC Storage']"
    )
    logging.info("Clicked on 'SBC Storage'.")