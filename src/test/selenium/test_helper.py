# test_helper.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def register(driver, username, password):
    # Click on the "Account" button to make the "register-button" visible
    account_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dropbtn")))
    account_button.click()

    # Find the register button and click it to open the registration form
    register_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "register-button")))
    register_button.click()

    # Fill in the username and password
    username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "r-username")))
    password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "r-password")))
    username_field.send_keys(username) # Placeholder username
    password_field.send_keys(password) # Placeholder password

    # Submit the form
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "r-submit")))
    submit_button.click()

    # Wait for logout button to appear to confirm successful registration and login
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logout-button")))
    
def login(driver, username, password):
    # Hover over the "Account" button to make the "login-button" visible
    account_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dropbtn")))
    ActionChains(driver).move_to_element(account_button).perform()

    # # Click on the account button to open the dropdown or menu
    # account_button.click()

    # Now the login button should be clickable
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login-button")))
    login_button.click()

    # Fill in the username and password
    username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "l-username")))
    password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "l-password")))
    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)

    # Submit the form
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "l-submit")))
    submit_button.click()

    # Wait for the login button to become invisible, indicating that the login menu has closed
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "login-button")))