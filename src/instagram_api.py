import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from typing import Dict
import time
import random

# Instagram implementation will be added below

class FacebookUser:
    def __init__(self, first_name: str, last_name: str, password: str, day: int, month: int, year: int, gender: str):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.day = day
        self.month = month
        self.year = year
        self.gender = gender
        self.email = None  # This will be set later with the temp email

class FacebookRegistration:
    def __init__(self):
        self.fb_driver = self.setup_driver()
        self.email_driver = self.setup_driver()
        self.wait_fb = WebDriverWait(self.fb_driver, 15)
        self.wait_email = WebDriverWait(self.email_driver, 15)

    def setup_driver(self):
        chrome_options = Options()
        return webdriver.Chrome(executable_path="../chromedriver.exe", options=chrome_options)

    def get_temp_email(self):
        self.email_driver.get("https://temp-mail.org/en/")
        try:
            # Wait for the email field to be present
            email_field = self.wait_email.until(EC.presence_of_element_located((By.ID, "mail")))

            # Define a custom condition to wait for a non-"Loading..." value
            def email_loaded(driver):
                email_value = email_field.get_attribute("value")
                return email_value != "" and "Loading" not in email_value

            # Wait for the email to be loaded (timeout after 30 seconds)
            WebDriverWait(self.email_driver, 15).until(email_loaded)

            # Get the email value
            email = email_field.get_attribute("value")
            print(f"Temporary email obtained: {email}")
            return email
        except Exception as e:
            print(f"Failed to get temporary email: {str(e)}")
            return None

    def start_facebook_registration(self, user: FacebookUser):
        self.fb_driver.get("https://www.facebook.com/r.php")
        self.accept_cookies(self.fb_driver)

        # Fill in the form fields
        self.human_like_type(self.fb_driver, "firstname", user.first_name)
        time.sleep(random.uniform(0.5, 1.5))
        self.human_like_type(self.fb_driver, "lastname", user.last_name)
        time.sleep(random.uniform(0.5, 1.5))
        self.human_like_type(self.fb_driver, "reg_email__", user.email)
        time.sleep(random.uniform(0.5, 1.5))

        # Wait for and fill the email confirmation field
        self.wait_fb.until(EC.presence_of_element_located((By.NAME, "reg_email_confirmation__")))
        self.human_like_type(self.fb_driver, "reg_email_confirmation__", user.email)
        time.sleep(random.uniform(0.5, 1.5))

        self.human_like_type(self.fb_driver, "reg_passwd__", user.password)
        time.sleep(random.uniform(0.5, 1.5))

        # Fill birthday
        self.select_dropdown("birthday_day", str(user.day))
        self.select_dropdown("birthday_month", str(user.month))
        self.select_dropdown("birthday_year", str(user.year))

        # Select gender
        self.select_gender(user.gender)

        print("Form filled. Please review and make any necessary changes.")
        # Click the sign up button
        signup_button = self.fb_driver.find_element(By.NAME, "websubmit")
        signup_button.click()

    def select_dropdown(self, name: str, value: str):
        dropdown = self.fb_driver.find_element(By.NAME, name)
        for option in dropdown.find_elements(By.TAG_NAME, 'option'):
            if option.get_attribute('value') == value:
                option.click()
                time.sleep(random.uniform(0.3, 0.7))
                break

    def select_gender(self, gender: str):
        try:
            if gender.lower() == "female":
                gender_radio = self.fb_driver.find_element(By.XPATH, "//input[@name='sex' and @value='1']")
            elif gender.lower() == "male":
                gender_radio = self.fb_driver.find_element(By.XPATH, "//input[@name='sex' and @value='2']")
            else:
                gender_radio = self.fb_driver.find_element(By.XPATH, "//input[@name='sex' and @value='-1']")

            gender_radio.click()
            time.sleep(random.uniform(0.3, 0.7))
        except Exception as e:
            print(f"Error selecting gender: {str(e)}")

    def get_confirmation_code(self):
        try:
            # Wait for the email from Facebook to appear
            facebook_email_xpath = "//span[contains(text(), 'is your Facebook confirmation code')]"
            self.wait_email.until(EC.presence_of_element_located((By.XPATH, facebook_email_xpath)))

            # Click on the Facebook email
            facebook_email = self.email_driver.find_element(By.XPATH, facebook_email_xpath)
            facebook_email.click()

            # Wait for the email content to load
            email_content_xpath = "//div[contains(@class, 'inbox-data-content-intro')]"
            email_content = self.wait_email.until(EC.presence_of_element_located((By.XPATH, email_content_xpath)))

            # Extract the confirmation code
            email_text = email_content.text
            match = re.search(r'FB-(\d+)', email_text)

            if match:
                confirmation_code = match.group(1)
                print(f"Confirmation code: {confirmation_code}")
                print("Please type this code into Facebook.")
                return confirmation_code
            else:
                print("Confirmation code not found in the email.")
                return None

        except Exception as e:
            print(f"Failed to get confirmation code: {str(e)}")
            return None
    def accept_cookies(self, driver):
        try:
            cookie_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Allow all cookies') or contains(., 'Accept all')]")))
            cookie_button.click()
        except TimeoutException:
            print("Cookie acceptance dialog not found or already accepted.")

    def human_like_type(self, driver, name: str, value: str):
        try:
            field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, name)))
            field.clear()
            for char in value:
                field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.2))
                if random.random() < 0.05:
                    time.sleep(random.uniform(0.5, 1))
        except Exception as e:
            print(f"Error filling {name}: {str(e)}")

    def spawn_new_user(self, first_name: str, last_name: str, password: str, day: int, month: int, year: int, gender: str) -> Dict[str, str]:
        user = FacebookUser(first_name, last_name, password, day, month, year, gender)

        user.email = self.get_temp_email()
        if not user.email:
            return {"status": "error", "message": "Failed to get temporary email"}

        self.start_facebook_registration(user)

        input("Press Enter when you're ready to retrieve the confirmation code...")
        confirmation_code = self.get_confirmation_code()

        if confirmation_code:
            print("Please enter the confirmation code in Facebook.")
            print(confirmation_code)
            input("Press Enter when you've completed the registration process...")
            return {"status": "success", "message": "User registration process completed"}
        else:
            return {"status": "error", "message": "Failed to get confirmation code"}

    def __del__(self):
        if hasattr(self, 'fb_driver'):
            self.fb_driver.quit()
        if hasattr(self, 'email_driver'):
            self.email_driver.quit()

# Example usage
if __name__ == "__main__":
    registration = FacebookRegistration()
    result = registration.spawn_new_user(
        first_name="Akseli",
        last_name="Kannan",
        password="securepassword123",
        day=15,
        month=6,
        year=1990,
        gender="male"
    )
    print(result)