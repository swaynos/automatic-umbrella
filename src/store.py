import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exceptions

import config
from utilities import take_screenshot, wait_for_element, click_when_clickable

def navigate_to_store(driver):
    # Wait for the navigation bar to be present
    wait_for_element(driver, By.CSS_SELECTOR, "nav.ut-tab-bar")
    # Click on the "SBC" button in the navigation bar
    click_when_clickable(driver, By.CSS_SELECTOR, "button.ut-tab-bar-item.icon-store")
    logging.info("Navigated to the store page.")

def click_on_packs(driver):
    # Wait for the "Packs" tile to be present
    wait_for_element(driver, By.XPATH, "//div[contains(@class, 'tile') and contains(@class, 'packs-tile')]")
    # Click on the "Packs" tile
    click_when_clickable(driver, By.XPATH, "//div[contains(@class, 'tile') and contains(@class, 'packs-tile')]")
    logging.info("Clicked on the 'Packs' tile.")

def click_ellipsis_button(driver):
    # Wait for the ellipsis button to be present
    ellipsis_button = wait_for_element(driver, By.CSS_SELECTOR, "button.ut-image-button-control.ellipsis-btn")
    ellipsis_button.click()
    logging.info("Clicked ellipsis button on unassigned items screen.")

def click_store_all_in_club(driver):
    # Wait for the "Store All in Club" button to be present
    store_all_button = wait_for_element(driver, By.XPATH, "//button[.//span[text()='Store All in Club']]")
    store_all_button.click()
    logging.info("Clicked 'Store All in Club' button.")

def find_pack_element(driver, pack_name, max_scroll_attempts=50):
    try:
        parent_div = wait_for_element(driver, By.CSS_SELECTOR, "div.ut-store-hub-view--content")
        scroll_attempts = 0

        while scroll_attempts < max_scroll_attempts:
            try:
                pack_element = parent_div.find_element(By.XPATH, f"//h1[@class='ut-store-pack-details-view--title']//span[text()='{pack_name}']")
                logging.info(f"Found pack: {pack_name}")
                return pack_element
            except selenium_exceptions.NoSuchElementException:
                driver.execute_script("arguments[0].scrollBy(0, 150);", parent_div)
                time.sleep(0.1)
                scroll_attempts += 1

        print(f"Reached max scroll attempts. Could not find pack: {pack_name}")
        return None
    except Exception as e:
        print(f"Could not find pack: {pack_name}. Error: {str(e)}")
        return None

def claim_pack(driver, pack_element):
    claim_button = pack_element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'ut-store-pack-details-view')]//span[contains(@class, 'subtext') and text()='Claim your Pack']")
    claim_button.click()
    logging.info("Clicked 'Claim your Pack' button.")
    check_for_unassigned_items_popup(driver)

    time.sleep(1)  # Wait for the unassigned items screen to load
    click_ellipsis_button(driver)
    click_store_all_in_club(driver)
    time.sleep(2)  # Wait for the action to process
    resolve_duplicates(driver)
    print("claim pack completed")

def scroll_to_top(driver):
    parent_div = wait_for_element(driver, By.CSS_SELECTOR, "div.ut-store-hub-view--content")
    driver.execute_script("arguments[0].scrollTo(0, 0);", parent_div)
    time.sleep(1)  # Allow time for the page to scroll to the top
    logging.info("Scrolled to the top of the page.")

def open_packs_by_name(driver, pack_name):
    while True:
        pack_element = find_pack_element(driver, pack_name)
        if pack_element:
            claim_pack(driver, pack_element)
            return True
        else:
            return False

def check_for_unassigned_items_popup(driver):
    try:
        # Wait for the popup to be present
        popup = driver.find_element(By.CSS_SELECTOR, "section.ea-dialog-view.ea-dialog-view-type--message")
        if popup.is_displayed():
            message = popup.find_element(By.CSS_SELECTOR, "header > h1").text
            if message == "Unassigned Items Remain":
                raise Exception("Unassigned Items Remain popup detected.")
        logging.info("No unassigned items found.")
    except selenium_exceptions.NoSuchElementException:
        # Popup not found, continue normally
        pass

def verify_duplicates_screen(driver):
    try:
        # Check if the "Duplicates" header is present within the specified structure
        driver.find_element(By.XPATH, "//header[@class='ut-section-header-view']//h2[@class='title' and text()='Untradeable Duplicates']")
        logging.info("Duplicates screen is being shown.")
        return True
    except selenium_exceptions.NoSuchElementException:
        logging.info("Duplicates screen is not being shown.")
        return False

def click_ellipsis_button_on_duplicates_screen(driver):
    # Wait for the ellipsis button in the header to be present
    ellipsis_button = wait_for_element(driver, By.XPATH, "//header[@class='ut-section-header-view']//button[contains(@class, 'ellipsis-btn')]")
    ellipsis_button.click()
    logging.info("Clicked ellipsis button on duplicates screen.")

def select_swap_in_all_tradeable_button(driver):
    # Wait for the "Swap in all Tradeable Duplicate items" button to be present
    swap_button = wait_for_element(driver, By.XPATH, "//div[@class='ut-bulk-action-popup-view']//button[.//span[text()='Swap in all Tradeable Duplicate items']]")
    swap_button.click()
    logging.info("Selected 'Swap in all Tradeable Duplicate items' button.")

def resolve_duplicates(driver):
    if verify_duplicates_screen(driver):
        click_ellipsis_button_on_duplicates_screen(driver)
        select_swap_in_all_tradeable_button(driver)
        time.sleep(.5) # Wait for action to process
        confirm_swap_items(driver)
        time.sleep(1.5) # Wait for action to process
        click_ellipsis_button_on_duplicates_screen(driver)
        time.sleep(.5)
        quick_sell_duplicates(driver)
        confirm_quick_sell(driver)

def quick_sell_duplicates(driver):
    # Wait for the "Quick Sell tradeable items for..." button to be present
    quick_sell_button = wait_for_element(driver, By.XPATH, "//div[@class='ut-bulk-action-popup-view']//button[.//span[contains(text(), 'Quick Sell')]]")
    quick_sell_button.click()
    # TODO: Sometimes there are two quick sell entries. One to quick sell for a coin profit,
    # plus another entry to quick sell for 0 coins
    logging.info("Clicked 'Quick Sell' item.")

def confirm_swap_items(driver):
    # Wait for the "Yes" button on the "Swap Items" confirmation popup to be present
    yes_button = wait_for_element(driver, By.XPATH, "//div[@class='ut-action-confirmation-popup-view']//button[.//span[text()='Yes']]")
    yes_button.click()
    logging.info("Confirmed swap items.")

def confirm_quick_sell(driver):
    # Wait for the "OK" button on the Quick Sell confirmation modal to be present
    ok_button = wait_for_element(driver, By.XPATH, "//section[@class='ea-dialog-view ea-dialog-view-type--message']//button[.//span[text()='Ok']]")
    ok_button.click()
    logging.info("Confirmed quick sell.")

def open_packs(driver):
    try:
        navigate_to_store(driver)
        click_on_packs(driver)
        for pack_name in config.PACK_NAMES:
            while True:
                scroll_to_top(driver)
                if not open_packs_by_name(driver, pack_name):
                    break
                navigate_to_store(driver)
                click_on_packs(driver)
    #Consider the following exception:
    #ERROR - Message: element click intercepted: Element <div class="tile ut-tile-view--with-gfx col-1-2 packs-tile storehub-tile highlight" style="">...</div> is not clickable at point (426, 276). Other element would receive the click: <div class="ut-click-shield showing">...</div>
    #    Proposal: If this element is visible, then wait before proceeding.
    
    except selenium_exceptions.TimeoutException as e:
        take_screenshot(driver)
        logging.error(f"Timeout Exception occurred: {e}")
    except Exception as e:
        error_message = str(e)
        take_screenshot(driver)
        logging.error(error_message)
    # TODO: Consider retrying on exception