import logging

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exceptions
import config
import time

from sbc_helpers import *
from utilities import *

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
        logging.error("Maximum retry attempts reached. Terminating toty crafting upgrade.")

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
        logging.error("Maximum retry attempts reached. Terminating grassroot grind challenges.")

#81+ 3 of 5 Player Pick
def eightyone_plus_player_pick(driver, use_sbc_storage = True):
    #TODO: There is some duplicate code here. Consider refactoring into a common wrapper.
    retry_attempts = 0
    max_retry_attempts = 3

    while retry_attempts < max_retry_attempts:
        try:
            quality = "Gold"
            sort_type = "Lowest Quick Sell"
            navigate_to_sbc(driver)
            select_upgrades_menu(driver)
            sbc_completable = open_daily_upgrade(driver, "81+ 3 of 5 Player Pick")
            if sbc_completable > 0 and not use_sbc_storage:
                for i in range(sbc_completable):
                    sbc_completable = open_daily_upgrade(driver, "81+ 3 of 5 Player Pick")
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
                            set_rarity(driver, "Rare")
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
        logging.error("Maximum retry attempts reached. Terminating 81+ challenge.")

def gold_upgrade(driver, repeats = 1,use_sbc_storage = True):
    challenge_name = "Gold Upgrade"
    logging.info(f"Starting {challenge_name} challenge.")
    retry_attempts = 0
    max_retry_attempts = 3

    while retry_attempts < max_retry_attempts:
        try:
            quality = "Gold"
            sort_type = "Lowest Quick Sell"
            navigate_to_sbc(driver)
            select_upgrades_menu(driver)
            for i in range(repeats):
                open_daily_upgrade(driver, challenge_name)
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
                        if use_sbc_storage:
                            set_sbc_storage(driver)
                        set_sorting_and_quality(driver, sort_type, quality)
                        set_rarity(driver, "Common")
                        close_active_filter_by_position(driver, selected_position)
                        click_search_button(driver)
                        time.sleep(1)
                        click_first_add_player(driver)
                        time.sleep(.5)
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
        logging.error("Maximum retry attempts reached. Terminating 81+ challenge.")
