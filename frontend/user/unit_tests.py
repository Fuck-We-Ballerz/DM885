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

        # Go to landing page
        driver.get("http://localhost/student/landing")
        
        # Click the register button
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Register"))
        ).click()
        
        # Wait for the registration form to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        # Register a new user
        username = "testuser" + str(int(time.time()))
        password = "testpassword"
        
        driver.find_element(By.NAME, "first_name").send_keys("Test")
        driver.find_element(By.NAME, "last_name").send_keys("User")
        driver.find_element(By.NAME, "email").send_keys(username + "@example.com")
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
    
        # Click the register button
        driver.find_element(By.XPATH, "//button[text()='Register']").click()

        # Wait for registration to complete and redirect to login page
        #time.sleep(2)
        
        
        # Wait for the username field to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        
        # Click the login button
        driver.find_element(By.XPATH, "//*[@id=\"kc-login\"]").click()   

        # Wait for login to complete and dashboard page to load
        #time.sleep(2)
        
        # Click on the specific assignment link
        assignment_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/a/div'))
        )
        assignment_link.click()

        #click this /html/body/div[2]/a/div

        
        # Wait for the assignment page to load
        #time.sleep(2)
        
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

        #time.sleep(2)
        
        # click the "Ok" button on the alert'
        WebDriverWait(driver, 10).until(
            EC.alert_is_present()
        ).accept()
        
        time.sleep(2)

        # Log out
        upload_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/div/a"))
        )
        upload_button.click()
        
        # Wait for the logout to complete
        #time.sleep(2)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
