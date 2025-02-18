import logging

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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
                logging.info(f"{upgrade_name} is already complete.")
                return 0  # Indicate that the task is complete with 0 repeatable count

            # Extract the repeatable count
            repeatable_element = parent_div.find_element(By.CSS_SELECTOR, "div.ut-squad-building-set-status-label-view.repeat span.text")
            repeatable_text = repeatable_element.text
            repeatable_count = int(repeatable_text.split(" ")[1])
            logging.info(f"Repeatable count for {upgrade_name}: {repeatable_count}")

            if repeatable_count == 0:  
                return 0

            # Click the upgrade header
            upgrade_header.click()
            logging.info(f"Clicked the {upgrade_name} upgrade.")

            # Check if the "Submit" button is enabled
            # TODO: Is this needed?
            # try:
            #     submit_button = driver.find_element(By.XPATH, "//button[contains(@class, 'ut-squad-tab-button-control') and contains(., 'Submit')]")
            #     if submit_button.get_attribute("disabled") is None:
            #         logging.warning(f"The 'Submit' button is not disabled for {upgrade_name}. Was it completed before?")
            #         return 1
                
            # except selenium_exceptions.NoSuchElementException:
            #     logging.error("Submit button not found after clicking the upgrade.")

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
            time.sleep(1)  # Allow the SBC an opportunity to load
                      
            # Check if the "Submit" button is present
            try:
                submit_button = driver.find_element(By.XPATH, "//button[contains(@class, 'ut-squad-tab-button-control') and contains(., 'Submit')]")
                if submit_button.is_displayed() and submit_button.is_enabled():
                    submit_button.click()  # Click the Submit button
                    logging.info(f"Clicked 'Submit' button without going through squad building steps.")
                    claim_rewards(driver)
                    continue  # Skip to the next iteration
            except selenium_exceptions.NoSuchElementException:
                logging.info("Submit button not found, proceeding with squad building.")

            # TODO: What to wait for above instead of sleep?
            if (select_position(driver, position)):
                time.sleep(1) # TODO: What to wait for instead?
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
                toggle_ignore_position(driver)
                time.sleep(.5) # Let the toggle complete the animation
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
                toggle_ignore_position(driver)
                time.sleep(.5) # Let the toggle complete the animation
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
    retry_attempts = 0
    max_retry_attempts = 3

    while retry_attempts < max_retry_attempts:
        try:
            sort_type = "Lowest Quick Sell"
            for simple_upgrade_name in config.DAILY_SIMPLE_BRONZE_SBC_NAMES:
                daily_simple_upgrade(driver, simple_upgrade_name, sort_type, "Bronze")
            for simple_upgrade_name in config.DAILY_SIMPLE_SILVER_SBC_NAMES:
                daily_simple_upgrade(driver, simple_upgrade_name, sort_type, "Silver")
            daily_gold_upgrade(driver, sort_type)
            # If successful, break out of the loop
            break
        except selenium_exceptions.TimeoutException as e:
            take_screenshot(driver)
            logging.error(f"Timeout Exception occurred: {str(e)}")
        except Exception as e:
            take_screenshot(driver)
            logging.error(f"An error occurred: {str(e)}")

        # Increment the retry attempt count and wait before retrying
        retry_attempts += 1
        logging.info(f"Retrying... Attempt {retry_attempts}/{max_retry_attempts}")

        # Optional: Add a delay before the next retry (e.g., time.sleep(2))
    
    if retry_attempts == max_retry_attempts:
        logging.error("Maximum retry attempts reached. Terminating daily challenges.")

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

def toty_crafting_upgrade(driver, use_sbc_storage = False):
    #TODO: There is some duplicate code here. Consider refactoring into a common wrapper.
    retry_attempts = 0
    max_retry_attempts = 3

    while retry_attempts < max_retry_attempts:
        try:
            quality = "Gold"
            sort_type = "Lowest Quick Sell"
            navigate_to_sbc(driver)
            select_upgrades_menu(driver)
            sbc_completable = open_daily_upgrade(driver, "TOTY Crafting Upgrade")
            if sbc_completable > 0 and not use_sbc_storage:
                for i in range(sbc_completable):
                    sbc_completable = open_daily_upgrade(driver, "TOTY Crafting Upgrade")
                    time.sleep(1)
                    # Find the first open slot
                    for index in range(0, 11):
                        # Hide the popover if it's visible
                        if sbc_requirements_popover_visible(driver):
                            click_when_clickable(driver, By.CSS_SELECTOR, "div.ut-squad-summary-info")

                        if is_slot_filled(driver, index):
                            continue
                        else:
                            # Set the first open slot to a Rare player
                            selected_position = select_position(driver, index=index)
                            if selected_position:
                                logging.info(f"Player selected at position: {selected_position}")
                                time.sleep(1) # TODO: What to wait for instead?
                                click_add_player_button(driver)
                                time.sleep(.5)  # Allow dropdown options to become visible
                                set_sorting_and_quality(driver, sort_type, quality)
                                set_rarity(driver, "Rare")
                                close_active_filter_by_position(driver, selected_position)
                                click_search_button(driver)
                                time.sleep(1)
                                click_first_add_player(driver)
                                time.sleep(.5)
                            # Click on the canvas to clear any dialogs
                            canvas = driver.find_element(By.CSS_SELECTOR, "canvas.ut-squad-pitch-view--canvas")
                            canvas.click()
                            break
                    # Fill the rest using squad builder
                    use_squad_builder(driver)
                    time.sleep(1)  # Allow dropdown options to become visible
                    toggle_ignore_position(driver)
                    set_sorting_and_quality(driver, sort_type, "Gold")
                    time.sleep(.5)
                    build_squad(driver)
                    time.sleep(2) # Allow requirements to update

                    check_sbc_requirements(driver)
                    # TODO: This could be high risk, check the ratings of the cards added before clicking submit
                    submit_squad(driver)
                    claim_rewards(driver)
            elif sbc_completable > 0 and use_sbc_storage:
                for i in range(sbc_completable):
                    time.sleep(1)
                    for index in range(0, 11):
                        # Hide the popover if it's visible
                        if sbc_requirements_popover_visible(driver):
                            click_when_clickable(driver, By.CSS_SELECTOR, "div.ut-squad-summary-info")

                        # If the slot is occupied, skip this interation and move onto the next index
                        if is_slot_filled(driver, index):
                            continue

                        selected_position = select_position(driver, index=index)
                        if selected_position:
                            logging.info(f"Player selected at position: {selected_position}")
                            time.sleep(1) # TODO: What to wait for instead?
                            click_add_player_button(driver)
                            time.sleep(.5)  # Allow dropdown options to become visible
                            set_sbc_storage(driver)
                            set_sorting_and_quality(driver, sort_type, quality)
                            close_active_filter_by_position(driver, selected_position)
                            click_search_button(driver)
                            time.sleep(1)
                            click_first_add_player(driver)
                            time.sleep(.5)

                        # TODO: Check the rarity of the players added. If a rare card was not added from SBC storage, attempt to add one from the player pool at index 11.
                        
                        else:
                            logging.error("Failed to add player.")
                    check_sbc_requirements(driver)

                    # TODO: This can be high risk, check the ratings of the cards added before clicking submit
                    submit_squad(driver)
                    claim_rewards(driver)
        except selenium_exceptions.TimeoutException as e:
            take_screenshot(driver)
            logging.error(f"Timeout Exception occurred: {str(e)}")
        except Exception as e:
            take_screenshot(driver)
            logging.error(f"An error occurred: {str(e)}")

        # Increment the retry attempt count and wait before retrying
        retry_attempts += 1
        logging.info(f"Retrying... Attempt {retry_attempts}/{max_retry_attempts}")
    
    if retry_attempts == max_retry_attempts:
        logging.error("Maximum retry attempts reached. Terminating daily challenges.")

def grassroot_grind(driver):
    retry_attempts = 0
    max_retry_attempts = 3

    while retry_attempts < max_retry_attempts:
        try:
            sort_type = "Lowest Quick Sell"
            navigate_to_sbc(driver)
            select_upgrades_menu(driver)
            sbc_completable = open_daily_upgrade(driver, "Grassroot Grind")
            for i in range(sbc_completable):
                sbc_completable = open_daily_upgrade(driver, "Grassroot Grind")
                time.sleep(1) # Allow the SBC an opportunity to load
                use_squad_builder(driver)
                time.sleep(1)  # Allow dropdown options to become visible
                toggle_ignore_position(driver)
                time.sleep(.5) # Let the toggle complete the animation
                set_sorting_and_quality(driver, sort_type, "Bronze")
                time.sleep(.5)
                build_squad(driver)
                time.sleep(2) # Allow requirements to update
                check_sbc_requirements(driver)
                submit_squad(driver)
                claim_rewards(driver)
        except selenium_exceptions.TimeoutException as e:
            take_screenshot(driver)
            logging.error(f"Timeout Exception occurred: {str(e)}")
        except Exception as e:
            take_screenshot(driver)
            logging.error(f"An error occurred: {str(e)}")

        # Increment the retry attempt count and wait before retrying
        retry_attempts += 1
        logging.info(f"Retrying... Attempt {retry_attempts}/{max_retry_attempts}")
    
    if retry_attempts == max_retry_attempts:
        logging.error("Maximum retry attempts reached. Terminating daily challenges.")