from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import config
import my_secrets as secrets

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the website
driver.get(config.APP_URL)

# Find the username and password fields and enter your credentials
username_field = driver.find_element(By.NAME, "username")
password_field = driver.find_element(By.NAME, "password")

username_field.send_keys(secrets.EMAIL)
password_field.send_keys(secrets.PASSWORD)

# Find the login button and click it
login_button = driver.find_element(By.NAME, "login")
login_button.click()

# Wait for the next page to load
driver.implicitly_wait(10)

# Perform additional tasks after logging in
# For example, navigate to a specific page
driver.get("https://example.com/specific-page")

# Perform actions on the new page
# For example, fill out a form or click a button
some_button = driver.find_element(By.ID, "some_button_id")
some_button.click()

# Close the browser when done
driver.quit()