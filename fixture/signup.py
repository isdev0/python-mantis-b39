import re
from selenium.webdriver.common.by import By


class SignupHelper:

    def __init__(self, app):
        self.app = app

    def new_user(self, username, password, email):
        wd = self.app.wd
        self.app.open_external_page(self.app.base_url + "/signup_page.php")
        wd.find_element(By.NAME, "username").send_keys(username)
        wd.find_element(By.NAME, "email").send_keys(email)
        wd.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        mail = self.app.mail.get_mail_by_subject(username, password, "[MantisBT] Account registration")
        url = self.extract_confirmation_url(mail)

        print("\nCONFIRMATION URL: [%s]" % url)

        wd.get(url)
        wd.find_element(By.NAME, "password").send_keys(password)
        wd.find_element(By.NAME, "password_confirm").send_keys(password)
        wd.find_element(By.CSS_SELECTOR, "input[value='Update User']").click()

    @staticmethod
    def extract_confirmation_url(text):
        return re.search("http://[\\w\\W]*[\\n\\n].\\n", text, re.MULTILINE).group(0).replace("\n", "")
        # return re.search("http://.*$", text, re.MULTILINE).group(0)
