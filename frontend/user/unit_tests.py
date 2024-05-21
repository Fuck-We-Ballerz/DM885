import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

class AssignmentSubmissionTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_register_login_submit(self):
        driver = self.driver

        driver.get("http://localhost/student/register")
        
        
        # Wait for the username field to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        # Register a new user
        username = "testuser" + str(int(time.time()))
        password = "testpassword"
        
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        
        # Wait for registration to complete and login page to load
        time.sleep(2)
        
        # Log in with the new user
        driver.get("http://localhost/student/login")
        
        # Wait for the username field to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        
                # Wait for login to complete and dashboard page to load
        time.sleep(2)
        
        # Click on the specific assignment link
        assignment_link_text = "coco: Final Project"
        assignment_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, assignment_link_text))
        )
        assignment_link.click()
        
        # Wait for the assignment page to load
        time.sleep(2)
        
        # Wait for the file input to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "file"))
        )
        
        file_input = driver.find_element(By.NAME, "file")
        
        # Create a temporary .zip file for testing
        zip_path = "/tmp/test_assignment.zip"
        with open(zip_path.replace('.zip', ''), "w") as f:
            f.write("Test content")
        os.system(f"zip -j {zip_path} {zip_path.replace('.zip', '')}")
        
        # Upload the .zip file
        file_input.send_keys(zip_path)
        
        # Click the upload button
        upload_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@onclick='attemptUpload()']"))
        )
        upload_button.click()

        # click the "Ok" button on the alert'
        WebDriverWait(driver, 10).until(
            EC.alert_is_present()
        ).accept()

        time.sleep(2)
        
        # click the "Ok" button on the alert'
        WebDriverWait(driver, 10).until(
            EC.alert_is_present()
        ).accept()
        
        time.sleep(2)

        # Log out
        driver.get("http://localhost/student/logout")
        
        # Wait for the logout to complete
        time.sleep(2)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
