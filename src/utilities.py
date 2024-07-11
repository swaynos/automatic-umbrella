import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config

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

def take_screenshot(driver):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = os.path.join("screenshots", f"error_{timestamp}.png")
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
    driver.save_screenshot(screenshot_path)