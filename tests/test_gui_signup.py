from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time, unittest,random, string, sqlite3

#Utility Function to fill in a SignUp text box
def fill_in_box(driver,field,content):
    username_box = driver.find_element_by_id(field)
    username_box.send_keys(content)

#Utility Function to fill in a submit a signup form
def submit(driver):
    submit_btn = driver.find_element_by_name('save_changes')
    submit_btn.click()
    time.sleep(3)

#Class to represent a user
class User:
    def __init__(self, username,email,password):
        self.username = username
        self.email = email
        self.password = password

class TestSignUp(unittest.TestCase):
    # Setup for each test - Opens a browser window
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:8000/_accounts/sign-up/')

    def tearDown(self):
        self.driver.close()

    #Testing Success Case
    def test_valid_user_is_accepted(self):
        valid_user = User('ValidUser','valid@email.com','Val1dPa55w0rd')
        fill_in_box(self.driver,'id_username',valid_user.username)
        fill_in_box(self.driver,'id_email',valid_user.email)
        fill_in_box(self.driver,'id_password1',valid_user.password)
        fill_in_box(self.driver,'id_password2',valid_user.password)
        submit(self.driver)
        new_url = self.driver.current_url
        self.assertTrue('_accounts/login/' in new_url)
        # Teardown for this test - Delets created user
        db_connection = sqlite3.connect('testproject/db/prepopulated.db')
        db_cursor = db_connection.cursor()
        db_cursor.execute('DELETE FROM auth_user WHERE username=\'ValidUser\'')
        db_connection.commit()
        db_connection.close()

    #Testing Failure Case - Invalid Username
    def test_invalid_usernames_are_rejected(self):
        invalid_characters = User('.Invalid/User','valid@email.com','Val1dPa55w0rd')
        fill_in_box(self.driver,'id_username',invalid_characters.username)
        fill_in_box(self.driver,'id_email',invalid_characters.email)
        fill_in_box(self.driver,'id_password1',invalid_characters.password)
        fill_in_box(self.driver,'id_password2',invalid_characters.password)
        submit(self.driver)
        notification = self.driver.find_element_by_id("error_1_id_username")
        self.assertTrue('characters' in notification.text)

    #Testing Failure Case - Passwords similar to username/email
    def test_similar_passwords_are_rejected(self):
        similar_passwords = User('UserWillBeRejected','UserWillBeRejected@email.com','UserWillBeRejected')
        fill_in_box(self.driver,'id_username',similar_passwords.username)
        fill_in_box(self.driver,'id_email',similar_passwords.email)
        fill_in_box(self.driver,'id_password1',similar_passwords.password)
        fill_in_box(self.driver,'id_password2',similar_passwords.password)
        submit(self.driver)
        notification = self.driver.find_element_by_id("error_1_id_password2")
        self.assertTrue('similar' in notification.text)

    #Testing Failure Case - Short Passwords
    def test_short_passwords_are_rejected(self):
        short_passwords = User('UserWillBeRejected','UserWillBeRejected@email.com','a')
        fill_in_box(self.driver,'id_username',short_passwords.username)
        fill_in_box(self.driver,'id_email',short_passwords.email)
        fill_in_box(self.driver,'id_password1',short_passwords.password)
        fill_in_box(self.driver,'id_password2',short_passwords.password)
        submit(self.driver)
        notification = self.driver.find_element_by_id("error_1_id_password2")
        self.assertTrue('8 characters' in notification.text)

    #Testing Failure Case - Numeric Passwords
    def test_numeric_passwords_are_rejected(self):
        numeric_passwords = User('UserWillBeRejected','UserWillBeRejected@email.com','24681012')
        fill_in_box(self.driver,'id_username',numeric_passwords.username)
        fill_in_box(self.driver,'id_email',numeric_passwords.email)
        fill_in_box(self.driver,'id_password1',numeric_passwords.password)
        fill_in_box(self.driver,'id_password2',numeric_passwords.password)
        submit(self.driver)
        notification = self.driver.find_element_by_id("error_1_id_password2")
        self.assertTrue('numeric' in notification.text)

    #Testing Failure Case - Invalid Emails are rejected
    def test_invalid_emails_are_rejected(self):
        invalid_emails = User('UserWillBeRejected','UserWillBeRejectedemail.com','24681012')
        fill_in_box(self.driver,'id_username',invalid_emails.username)
        fill_in_box(self.driver,'id_email',invalid_emails.email)
        fill_in_box(self.driver,'id_password1',invalid_emails.password)
        fill_in_box(self.driver,'id_password2',invalid_emails.password)
        submit(self.driver)
        new_url = self.driver.current_url
        self.assertFalse('_accounts/login/' in new_url)

    #Testing Failure Case - Mismatched Passwords
    def test_mismatched_passwords_are_rejected(self):
        mismatched_passwords = User('UserWillBeRejected','UserWillBeRejected@email.com','pa55w0rd')
        fill_in_box(self.driver,'id_username',mismatched_passwords.username)
        fill_in_box(self.driver,'id_email',mismatched_passwords.email)
        fill_in_box(self.driver,'id_password1',mismatched_passwords.password)
        fill_in_box(self.driver,'id_password2','password')
        submit(self.driver)
        notification = self.driver.find_element_by_id("error_1_id_password2")
        self.assertTrue('match' in notification.text)

if __name__ == '__main__':
    unittest.main()
