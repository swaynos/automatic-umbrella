import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading

import config

COOKIES_FILE = "cookies.json"

def wait_for_user_input(event):
    input("Press Enter to continue...")
    event.set()

def save_cookies(driver, cookies_file):
    with open(cookies_file, 'w') as file:
        json.dump(driver.get_cookies(), file)

def load_cookies(driver, cookies_file, target_domain):
    with open(cookies_file, 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            # Set the cookie's domain to the target domain (if necessary)
            cookie['domain'] = target_domain
            driver.add_cookie(cookie)

def is_logged_in(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, "nav.ut-tab-bar")
        return True
    except:
        return False

def login(driver):
    # Open the website
    driver.get(config.APP_URL)

    # Load cookies if they exist
    try:
        load_cookies(driver, COOKIES_FILE, ".ea.com")
        driver.refresh()
        if is_logged_in(driver):
            print("Logged in using cookies.")
            return
    except FileNotFoundError:
        pass
    except Exception as e:
        # Handle the exception if necessary
        print(f"An error occurred: {e}")
        raise e  

    # Wait for the login button to be clickable
    login_button = WebDriverWait(driver, config.LONGER_WAIT_DURATION).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-standard.call-to-action"))
    )

    # Click the login button
    login_button.click()

    # Wait for the email input to be visible
    email_input = WebDriverWait(driver, config.DEFAULT_WAIT_DURATION).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )

    # Enter email
    email_input.send_keys(config.EMAIL)

    # Check for the presence of the "NEXT" button and click it if present
    try:
        next_button = WebDriverWait(driver, config.DEFAULT_WAIT_DURATION).until(
            EC.element_to_be_clickable((By.ID, "logInBtn"))
        )
        next_button.click()  # Clicks the NEXT button
        # Wait for the password input to be visible
        password_input = WebDriverWait(driver, config.DEFAULT_WAIT_DURATION).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )

        # Enter password
        password_input.send_keys(config.PASSWORD)  # Replace with your password
    except Exception as e:
        print(f"NEXT button not found or could not be clicked: {e}")

    # Wait for the sign-in button to be clickable and click it
    sign_in_button = WebDriverWait(driver, config.DEFAULT_WAIT_DURATION).until(
        EC.element_to_be_clickable((By.ID, "logInBtn"))
    )
    
    # Click the sign-in button
    sign_in_button.click()

    # Wait for the 2FA form to be present if cookies are not used
    try:
        two_fa_form = WebDriverWait(driver, config.DEFAULT_WAIT_DURATION).until(
            EC.presence_of_element_located((By.ID, "otcForm"))
        )

        # Create an event to signal when the user presses Enter
        user_input_event = threading.Event()
        user_input_thread = threading.Thread(target=wait_for_user_input, args=(user_input_event,))
        user_input_thread.start()

        try:
            # Wait for either the navigation bar to be present or user input
            WebDriverWait(driver, config.DEFAULT_WAIT_DURATION).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "nav.ut-tab-bar")),
                    lambda driver: user_input_event.is_set()
                )
            )
        except Exception as e:
            print(f"An error occurred: {e}")

        # Ensure user input thread is joined
        user_input_thread.join()
    except:
        pass

    # Save cookies after successful login
    save_cookies(driver, COOKIES_FILE)