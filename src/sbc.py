import logging

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exceptions
import config
import time

from sbc_helpers import build_squad as helpers_build_squad
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
            # TODO: This sleep duration seems long. What to wait for instead?
            
            if presubmit_squad_if_available(driver):
                logging.info(f"'Submit' button clicked without going through squad building steps.")
                continue

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

# TODO: Move this to utilities after resolving TODOs.
def squad_builder_upgrade(driver, sort_type, quality):
    use_squad_builder(driver)
    # TODO: Don't sleep, wait for the necessary dropdown options 
    time.sleep(1)  # Allow dropdown options to become visible
    toggle_ignore_position(driver)

    # TODO: Wait for the animation to complete instead of sleeping
    time.sleep(.5) # Let the toggle complete the animation
    set_sorting_and_quality(driver, sort_type, quality)

    time.sleep(.5) # TODO: What are we sleeping for?

    helpers_build_squad(driver)
    time.sleep(2) # Allow requirements to update
    # TODO: This sleep duration is excessive. Is it even necessary?

    check_sbc_requirements(driver)
    submit_squad(driver)
    claim_rewards(driver)

def daily_gold_upgrade(driver, sort_type):
    navigate_to_sbc(driver)
    select_upgrades_menu(driver)
    sbc_completable = open_daily_upgrade(driver, "Daily Gold Upgrade")
    if sbc_completable > 0:
        for i in range(sbc_completable):
            time.sleep(1) # Allow the SBC an opportunity to load
            # Index 0 is locked out, so we let the first iteration be 5+1
            squad_success = build_squad_variable_rarity(driver, "Bronze", sort_type, False, 0, 6)
            if squad_success:
                # Index 1 through 5 are filled with bronze so set the limit to 6+5
                squad_success = build_squad_variable_rarity(driver, "Silver", sort_type, False, 0, 11)

            if squad_success:
                check_sbc_requirements(driver)
                submit_squad(driver)
                claim_rewards(driver)

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

# TODO: IMPORTANT. The functions below need to be refactored to use existing helpers, or define new helpers.
def special_crafting_upgrade(driver, SBC_NAME, use_sbc_storage = False):
    #TODO: There is some duplicate code here. Consider refactoring into a common wrapper.
    retry_attempts = 0
    max_retry_attempts = 3
    while retry_attempts < max_retry_attempts:
        try:
            quality = "Gold"
            sort_type = "Lowest Quick Sell"
            navigate_to_sbc(driver)
            select_upgrades_menu(driver)
            sbc_completable = open_daily_upgrade(driver, SBC_NAME)
            if sbc_completable > 0:
                for i in range(sbc_completable):
                    sbc_completable = open_daily_upgrade(driver, SBC_NAME)
                    time.sleep(1)
                    if build_squad(driver, quality, rarity = None, sort_type = sort_type, use_sbc_storage = use_sbc_storage):
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
    
    # It actually already terminated the loop, but we should log the error
    if retry_attempts == max_retry_attempts:
        logging.error("Maximum retry attempts reached. Terminating special crafting upgrade.")

def build_squad(driver, quality, rarity, sort_type, use_sbc_storage = True):
    for index in range(0, 11):
        # Hide the popover if it's visible
        if sbc_requirements_popover_visible(driver):
            click_when_clickable(driver, By.CSS_SELECTOR, "div.ut-squad-summary-info")

         # If the slot is occupied, skip this interation and move onto the next index
        if is_slot_filled(driver, index) or is_slot_locked(driver, index):
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
            if rarity:
                set_rarity(driver, rarity)
            close_active_filter_by_position(driver, selected_position)
            click_search_button(driver)
            time.sleep(1)
            click_first_add_player(driver)
            time.sleep(.5)
        else:
            logging.error("Failed to add player.")
            return False
    
    return True

# Effectively the same as build_squad, but with the ability to specify how many rare players to add
# TODO: This could/should be the same method as above if I'm okay with sending a rare_count instead of specifying a rarity...
def build_squad_variable_rarity(driver, quality, sort_type, use_sbc_storage = True, rare_count = 0, limit = 0):
    current_rare_count = 0
    upper_range = 11 if limit == 0 else limit
    for index in range(0, upper_range):
        # Hide the popover if it's visible
        if sbc_requirements_popover_visible(driver):
            click_when_clickable(driver, By.CSS_SELECTOR, "div.ut-squad-summary-info")

         # If the slot is occupied, skip this interation and move onto the next index
        if is_slot_filled(driver, index) or is_slot_locked(driver, index):
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
            if (current_rare_count < rare_count):
                rarity = "Rare"
                current_rare_count += 1
            else:
                rarity = "Common"
            set_rarity(driver, rarity)
            close_active_filter_by_position(driver, selected_position)
            click_search_button(driver)
            time.sleep(1)
            click_first_add_player(driver)
            time.sleep(.5)
        else:
            logging.error("Failed to add player.")
            return False
    
    return True


def gold_upgrade(driver, repeats = 1, use_sbc_storage = True):
    challenge_name = "Gold Upgrade"
    logging.info(f"Starting {challenge_name} challenge.")

    try:
        quality = "Gold"
        sort_type = "Lowest Quick Sell"
        navigate_to_sbc(driver)
        select_upgrades_menu(driver)
        for i in range(repeats):
            open_daily_upgrade(driver, challenge_name)
            time.sleep(1)
            if build_squad(driver, quality, "Common", sort_type, use_sbc_storage):
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

def special_upgrade(driver, challenge_name, repeats = 1, use_sbc_storage = True, rare_count = 1):
    logging.info(f"Starting {challenge_name} challenge.")

    try:
        quality = "Gold"
        sort_type = "Lowest Quick Sell"
        navigate_to_sbc(driver)
        select_upgrades_menu(driver)
        for i in range(repeats):
            open_daily_upgrade(driver, challenge_name)
            time.sleep(1)
            if build_squad_variable_rarity(driver, quality, sort_type, use_sbc_storage, rare_count):
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