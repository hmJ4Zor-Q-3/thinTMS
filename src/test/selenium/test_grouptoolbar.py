from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TestGroupToolbar(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1:5000")  # Replace with your website URL

    def test_create_group(self):
        driver = self.driver

        # Find the input field and button for creating a new group
        new_group_name_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "new-group-name")))
        create_group_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "create-group")))

        # Enter a new group name and click the button to create the group
        new_group_name_input.send_keys("Test Group")
        create_group_button.click()

        # Wait for the new group to be added to the groups container
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, "groups"), "Test Group"))

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()