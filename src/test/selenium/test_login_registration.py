import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class TestLoginRegistration(unittest.TestCase):
    def test_login(self):
        driver = webdriver.Firefox()  # or webdriver.Chrome()

        # Navigate to website
        driver.get("http://127.0.0.1:5000")

        # Hover over the "Account" button to make the "login-button" visible
        account_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dropbtn")))
        ActionChains(driver).move_to_element(account_button).perform()

        # Find the login button and click it to open the login form
        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login-button")))
        login_button.click()

        # Fill in the username and password
        username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "l-username")))
        password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "l-password")))
        username_field.send_keys("rcipriano") # Placeholder username
        password_field.send_keys("thinTMS2024!") # Placeholder password

        # Submit the form
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "l-submit")))
        submit_button.click()

        # Wait for the logout button to appear, indicating successful login
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logout-button")))

        driver.quit()
        
        def test_unsuccessful_login(self):
            driver = webdriver.Firefox()
            driver.get("http://127.0.0.1:5000")
            account_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dropbtn")))
            account_button.click()
            # login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login-button")))
            login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-button")))

            login_button.click()
            username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "l-username")))
            password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "l-password")))
            username_field.send_keys("wrongUsername")
            password_field.send_keys("wrongPassword")
            submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "l-submit")))
            submit_button.click()
            error_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "l-errors")))
            self.assertEqual(error_message.text, "Expected error message")
            driver.quit()


    def test_registration(self):
        driver = webdriver.Firefox()  # or webdriver.Chrome() / Firefox

        # Navigate to website
        driver.get("http://127.0.0.1:5000")

        # Click on the "Account" button to make the "register-button" visible
        account_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dropbtn")))
        account_button.click()

        # Find the register button and click it to open the registration form
        register_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "register-button")))
        register_button.click()

        # Fill in the username and password
        username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "r-username")))
        password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "r-password")))
        username_field.send_keys("testUser") # Placeholder username
        password_field.send_keys("Password1234!") # Placeholder password

        # Submit the form
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "r-submit")))
        submit_button.click()

        # Wait for logout button to appear to confirm successful registration and login
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logout-button")))

        driver.quit()
        
        def test_unsuccessful_registration(self):
            driver = webdriver.Firefox()
            driver.get("http://127.0.0.1:5000")
            account_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dropbtn")))
            account_button.click()
            register_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "register-button")))
            register_button.click()
            username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "r-username")))
            password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "r-password")))
            username_field.send_keys("existingUsername")
            password_field.send_keys("password1234!")
            submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "r-submit")))
            submit_button.click()
            error_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "r-errors")))
            self.assertEqual(error_message.text, "Expected error message")
            driver.quit()

    def test_navigation(self):
        driver = webdriver.Firefox()
        driver.get("http://127.0.0.1:5000")

        # Register a new user
        account_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dropbtn")))
        account_button.click()
        register_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "register-button")))
        register_button.click()
        username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "r-username")))
        password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "r-password")))
        username_field.send_keys("newUser") # Placeholder username
        password_field.send_keys("Password1234!") # Placeholder password
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "r-submit")))
        submit_button.click()

        # Wait for logout button to appear to confirm successful registration and login
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logout-button")))

        # Log out after registration
        logout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "logout-button")))
        logout_button.click()

        # Log in with the new user
        account_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "dropbtn")))
        account_button.click()
        login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-button")))
        login_button.click()
        username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "l-username")))
        password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "l-password")))
        username_field.send_keys("newUser") # Placeholder username
        password_field.send_keys("Password1234!") # Placeholder password
        submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "l-submit")))
        submit_button.click()

        # Wait for the login process to complete
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "logout-button")))

        # Hover over the "Account" button to make the "workspace-button" visible
        account_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dropbtn")))
        ActionChains(driver).move_to_element(account_button).perform()

        # Now our user should be logged in, and the workspace button should be clickable
        # (Might be unnecessary here)
        workspace_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "workspace-button")))
        workspace_button.click()

        self.assertEqual(driver.current_url, "http://127.0.0.1:5000/workspace")
        driver.quit()

    def test_ui_elements(self):
        driver = webdriver.Firefox()
        driver.get("http://127.0.0.1:5000")
        account_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dropbtn")))
        login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-button")))
        register_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "register-button")))
        driver.quit()

if __name__ == "__main__":
    unittest.main()