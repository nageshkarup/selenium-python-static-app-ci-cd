import os
import shutil
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium.webdriver.chrome.options import Options as ChromeOptions

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/static")

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

    # Create a temporary directory for the user data
    user_data_dir = tempfile.mkdtemp()

    try:
        chrome_options = ChromeOptions()
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

        driver = webdriver.Chrome(
            options=chrome_options
        )
        driver.maximize_window()

    finally:
        # Ensure the directory is removed after the session
        shutil.rmtree(user_data_dir)

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
