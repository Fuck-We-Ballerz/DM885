import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os
import time

class AssignmentSubmissionTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_register_login_submit(self):
        driver = self.driver

        
        local = True
        if local:
            # Go to landing page
            driver.get("https://localhost/")

            # Skip the SSL warning
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"details-button\"]"))
            ).click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id=\"proceed-link\"]"))
            ).click()
        else:
            driver.get("https://zeruscloud/")


        # Login as admin 
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/button[3]"))
        ).click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_admin = "admin"
        password_admin = "admin"
        driver.find_element(By.NAME, "username").send_keys(username_admin)
        driver.find_element(By.NAME, "password").send_keys(password_admin)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"kc-login\"]"))
        ).click()

        # Create a teacher
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/nav/a[1]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "firstName"))
        )
        teacher_username = "teacher" + str(int(time.time()))
        driver.find_element(By.NAME, "firstName").send_keys("teacher")
        driver.find_element(By.NAME, "lastName").send_keys("test")
        driver.find_element(By.NAME, "username").send_keys(teacher_username)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/form/button[1]"))
        ).click()

        # Log out
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/nav/a[4]"))
        ).click()

        # Login as teacher
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/button[2]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        driver.find_element(By.NAME, "username").send_keys(teacher_username)
        driver.find_element(By.NAME, "password").send_keys("pass")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"kc-login\"]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password-new"))
        )
        teacher_password = "test" + str(int(time.time()))
        driver.find_element(By.NAME, "password-new").send_keys(teacher_password)
        driver.find_element(By.NAME, "password-confirm").send_keys(teacher_password)

        # Wait for the registration form to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"kc-form-buttons\"]/input"))
        ).click()
        email = teacher_username + "@example.com"
        driver.find_element(By.NAME, "email").send_keys(email)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"kc-form-buttons\"]/input"))
        ).click()

        # Log out
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/nav/a[4]"))
        ).click()

        # Create a student
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/button[1]"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/a[2]"))
        ).click()
        
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
        
        # Wait for the username field to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        
        # Click the login button
        driver.find_element(By.XPATH, "//*[@id=\"kc-login\"]").click()   

        # Log out
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/div/a"))
        ).click()

        # Login as teacher
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/button[2]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(teacher_username)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        ).send_keys(teacher_password)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"kc-login\"]"))
        ).click()

        # Create a course
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/nav/a[1]"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/nav[2]/a[1]"))
        ).click()
        course_name = "test_course" + str(int(time.time()))
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "courseName"))
        ).send_keys(course_name)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/form/button[1]"))
        ).click()


        # Assign students to the course
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/nav[2]/a[2]"))
        ).click()

        # Select the course
        course_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"course\"]"))
            )
        for option in course_select.find_elements(By.TAG_NAME, "option"):
            if option.text == course_name:
                option.click()
                break

        try:
            # Locate the row containing the username
            user_row = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//tr[td[contains(text(), '{username}')]]"))
            )
            
            # Locate the checkbox within that row and click it
            checkbox = user_row.find_element(By.XPATH, ".//input[@type='checkbox']")
            checkbox.click()

        except Exception as e:
            print(f"An error occurred: {e}")
        # Submit 
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/form/button"))
        ).click()
        time.sleep(2)
        # Click assignment button
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/nav[1]/a[2]"))
        ).click()
        time.sleep(2)
        # Create an assignment
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/nav[2]/a[1]"))
        ).click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div[1]/div[2]"))
        )
        # Check if there are any existing configurations
        config_table = None
        try:
            config_table = driver.find_element(By.XPATH, "//div[contains(., 'Config')]/table")
        except Exception as e:
            pass
        
        if not config_table:
            # If no configurations are found, click the "Add Configuration" button
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div[1]/div[1]/form/button"))
            ).click()

        # Wait for the form to be present
        form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div[2]/form"))
        )
        
        assignment_title = "Assignment Title"
        # Fill in the title
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"title\"]"))
        ).send_keys(assignment_title)

        # Select a course
        course_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"course\"]"))
        )
        for option in course_select.find_elements(By.TAG_NAME, "option"):
            if option.text == course_name:
                option.click()
                break

        # Fill in the Docker image
        docker_image_textarea = form.find_element(By.ID, "docker-image")
        docker_image_textarea.send_keys("Some Docker image")

        # Fill in the start date
        start_date_input = form.find_element(By.ID, "startDate")
        start_date_input.send_keys("06-17-2024")

        # Fill in the due date
        due_date_input = form.find_element(By.ID, "dueDate")
        due_date_input.send_keys("06-21-2024")

        # Select an assignment configuration
        assignment_config_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "assignmentConfig"))
        )
        for option in assignment_config_select.find_elements(By.TAG_NAME, "option"):
            if option.text.__contains__("Config"):
                option.click()
                break


        # Click the create button
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div[2]/form/div/button[1]"))
        ).click()

        time.sleep(2)
        # Assign the assignment to the student
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/nav[2]/a[3]"))
        ).click()
        time.sleep(2)

        # Select the course
        course_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"course\"]"))
            )
        for option in course_select.find_elements(By.TAG_NAME, "option"):
            if option.text == course_name:
                option.click()
                break
        

        # Click the "Add Students" button
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/form/button"))
        ).click()

        # Wait for the "Add Students" form to be present
        add_students_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//form[contains(@method, 'post')]"))
        )

        # Select the assignment
        assignment_select = add_students_form.find_element(By.ID, "assignment")
        for option in assignment_select.find_elements(By.TAG_NAME, "option"):
            if option.text == assignment_title:
                option.click()
                break

        # Locate the row containing the username
        user_row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//tr[td[contains(text(), '{username}')]]"))
        )
        
        # Locate the checkbox within that row and click it
        checkbox = user_row.find_element(By.XPATH, ".//input[@type='checkbox']")
        checkbox.click()

        # Click the submit button
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/form/button"))
        ).click()
        time.sleep(2)
        # Log out
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/nav[1]/a[4]"))
        ).click()

        # Login as student
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/button[1]"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/a[1]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"kc-login\"]"))
        ).click()

        # Click on the specific assignment link
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/a/div'))
        ).click()

        # Wait for the file input to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"zipFileUpload\"]"))
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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@onclick='attemptUpload()']"))
        ).click()

        # Click the "Ok" button on the alert
        WebDriverWait(driver, 10).until(
            EC.alert_is_present()
        ).accept()

        # Click the "Ok" button on the alert
        WebDriverWait(driver, 10).until(
            EC.alert_is_present()
        ).accept()


        time.sleep(2)

        # Log out
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/div/a"))
        ).click()
        


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
