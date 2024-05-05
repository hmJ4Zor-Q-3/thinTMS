import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from test_helper import register
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException


# Test in terminal with the following command: python -m unittest src/test/selenium/test_workspace.py

class TestWorkspace(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1:5000")  # Go to the homepage

        # Generate a unique username
        self.username = "testUser" + str(int(time.time()))

        # Register a new user
        register(self.driver, self.username, "testPassword2024!")

        # Hover over the "Account" button to make the "workspace-button" visible
        account_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dropbtn")))
        ActionChains(self.driver).move_to_element(account_button).perform()

        # Click the workspace button
        workspace_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "workspace-button")))
        workspace_button.click()

    def test_group_creation(self):
        # Test the "Create Group" button
        new_group_name = "Test Group"
        self.driver.find_element(By.ID, "new-group-name").send_keys(new_group_name)
        self.driver.find_element(By.ID, "create-group").click()

        # Wait for the new group to be added to the select dropdown
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#group-select option:last-child"), new_group_name))

    def test_task_creation(self):
        # Create the group before selecting it
        self.test_group_creation()

        # Select the group before adding a task
        select = Select(self.driver.find_element(By.ID, "group-select"))
        select.select_by_visible_text("Test Group")

        # Test the task creation form
        self.driver.find_element(By.ID, "task-name").send_keys("Test Task")
        self.driver.find_element(By.ID, "task-desc").send_keys("This is a test task.")
        self.driver.find_element(By.ID, "due-date").send_keys("2022-12-31")
        self.driver.find_element(By.ID, "new-task-time").send_keys("12:00")
        self.driver.find_element(By.ID, "add-task").click()

        # Wait for the new task to be added to the task list
        WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#task-list li:last-child"), "Test Task"))

    def test_group_creation_with_empty_name(self):
        # Try to create a group with an empty name
        self.driver.find_element(By.ID, "new-group-name").send_keys("")
        self.driver.find_element(By.ID, "create-group").click()

        # Check if an alert is displayed
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.assertEqual(alert.text, 'Group name must contain at least one non-whitespace character.')
            alert.accept()
        except TimeoutException:
            self.fail("Alert did not appear.")

    def test_task_creation_without_group(self):
    # Try to create a task without selecting a group
        self.driver.find_element(By.ID, "task-name").send_keys("Test Task")
        self.driver.find_element(By.ID, "task-desc").send_keys("This is a test task.")
        self.driver.find_element(By.ID, "due-date").send_keys("2022-12-31")
        self.driver.find_element(By.ID, "new-task-time").send_keys("12:00")
        self.driver.find_element(By.ID, "add-task").click()

    # Check if an alert is displayed
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.assertEqual(alert.text, "Please select a group before adding a task.")
            alert.accept()
        except TimeoutException:
            self.fail("Alert did not appear.")
    
    
   # Could not get these tests to work
   # def test_edit_task(self):
   #     # Create a task before editing it
   #     self.test_task_creation()
   #
   #     # Wait for the edit button to be available and click it
   #     edit_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#task-list li:last-child .edit-task")))
   #     edit_button.click()
   #
   #     # Wait for the edit form to appear and fill it out
   #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "task-form")))
   #     self.driver.find_element(By.ID, "task-name").clear()
   #     self.driver.find_element(By.ID, "task-name").send_keys("Edited Task")
   #     self.driver.find_element(By.ID, "task-desc").clear()
   #     self.driver.find_element(By.ID, "task-desc").send_keys("This is an edited task.")
   #     self.driver.find_element(By.ID, "due-date").clear()
   #     self.driver.find_element(By.ID, "due-date").send_keys("2023-01-01")
   #     self.driver.find_element(By.ID, "new-task-time").clear()
   #     self.driver.find_element(By.ID, "new-task-time").send_keys("13:00")
   #     self.driver.find_element(By.ID, "add-task").click()
   #
   #     # Wait for the task list to be updated
   #     WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#task-list li:last-child"), "Edited Task"))
   #     
   # def test_delete_task(self):
   #     # Create a task before deleting it
   #     self.test_task_creation()

   #     # Wait for the delete button to be available and click it
   #     delete_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#task-list li .delete-task")))
   #     delete_button.click()

   #     # Click the delete button for the last task in the list
   #     self.driver.find_element(By.CSS_SELECTOR, ".delete_task").click()

   #     # Wait for the task to be removed from the task list
   #     WebDriverWait(self.driver, 10).until_not(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#task-list li"), "Test Task"))
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
    
# class TestWorkspace(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Firefox()
#         self.driver.get("http://127.0.0.1:5000")  # Go to the homepage

#     def test_workspace_functionality(self):
#         driver = self.driver

#         # Generate a unique username
#         username = "testUser" + str(int(time.time()))

#         # Register a new user
#         register(driver, username, "testPassword2024!")

#         # Hover over the "Account" button to make the "workspace-button" visible
#         account_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dropbtn")))
#         ActionChains(driver).move_to_element(account_button).perform()

#         # Click the workspace button
#         workspace_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "workspace-button")))
#         workspace_button.click()

#         # Test if the workspace page has loaded correctly
#         workspace_header = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "workspace-form-h2")))
#         self.assertEqual(workspace_header.text, "Add a New Task")

#         # Test if the task list is present
#         task_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "task-list")))
#         self.assertIsNotNone(task_list)

#         # Test the "Create Group" button
#         new_group_name = "Test Group"
#         driver.find_element(By.ID, "new-group-name").send_keys(new_group_name)
#         driver.find_element(By.ID, "create-group").click()

#         # Wait for the new group to be added to the select dropdown
#         WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#group-select option:last-child"), new_group_name))

#         # Test the task creation form
#         driver.find_element(By.ID, "group-select").send_keys(new_group_name)
#         driver.find_element(By.ID, "task-name").send_keys("Test Task")
#         driver.find_element(By.ID, "task-desc").send_keys("This is a test task.")
#         driver.find_element(By.ID, "due-date").send_keys("2022-12-31")
#         driver.find_element(By.ID, "new-task-time").send_keys("12:00")
#         driver.find_element(By.ID, "add-task").click()

#         # Wait for the new task to be added to the task list
#         WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#task-list li:last-child"), "Test Task"))

#         driver.quit()

# if __name__ == "__main__":
#     unittest.main()