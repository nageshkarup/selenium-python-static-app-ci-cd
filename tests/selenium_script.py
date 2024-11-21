import os
import shutil
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/static")
BROWSER_NAME = os.getenv("BROWSER_NAME", "chrome").lower()

# Define locators
LOCATORS = {
    "name": (By.ID, "name"),
    "email": (By.ID, "email"),
    "password": (By.ID, "password"),
    "signup_button": (By.XPATH, "//button"),
    "user_name": (By.ID, "userName"),
}

# Function to initialize the driver
@pytest.fixture(scope="module", autouse=True)
def driver():
    if BROWSER_NAME == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)
    elif BROWSER_NAME == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")  # Running Firefox in headless mode
        driver = webdriver.Firefox(options=firefox_options)
    else:
        raise ValueError(f"Unsupported browser: {BROWSER_NAME}")
    print(f"Starting {BROWSER_NAME} browser...")
    driver.maximize_window()

    yield driver
    driver.quit()

# Explicit wait function
def wait_for_element(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))

# Sign-up method
def sign_up(driver, name, email, password):
    driver.get(f"{BASE_URL}/index.html")
    wait_for_element(driver, LOCATORS["name"]).send_keys(name)
    wait_for_element(driver, LOCATORS["email"]).send_keys(email)
    wait_for_element(driver, LOCATORS["password"]).send_keys(password)
    wait_for_element(driver, LOCATORS["signup_button"]).click()

# Sign-in method
def sign_in(driver, email, password):
    wait_for_element(driver, LOCATORS["email"]).send_keys(email)
    wait_for_element(driver, LOCATORS["password"]).send_keys(password)
    wait_for_element(driver, LOCATORS["signup_button"]).click()

# Log out method
def log_out(driver):
    wait_for_element(driver, LOCATORS["signup_button"]).click()

# Test method to run the sign-up, sign-in, and assert the username
def test_sign_up_sign_in(driver):
    
    # Sign up
    sign_up(driver, "Test User", "test@example.com", "testpassword")
    
    # Sign in
    sign_in(driver, "test@example.com", "testpassword")
    
    # Check the username after sign in
    username = wait_for_element(driver, LOCATORS["user_name"]).text
    assert username == "Test User", f"Expected username to be 'Test User' but got {username}"

    # Log out
    log_out(driver)
