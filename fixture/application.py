from selenium import webdriver
from selenium.webdriver.common.by import By
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from fixture.srv_email import SrvEmailHelper
from fixture.signup import SignupHelper
from fixture.mail import MailHelper


class Application:

    def __init__(self, browser, config):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        elif browser == "edge":
            self.wd = webdriver.Edge()
        else:
            raise ValueError("Browser '%s' undefined" % browser)

        self.wd.maximize_window()
        self.wd.implicitly_wait(0.25)
        self.config = config
        self.base_url = self.config["web"]["base_url"]
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.srv_email = SrvEmailHelper(self)
        self.signup = SignupHelper(self)
        self.mail = MailHelper(self)

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_internal_page(self, tab):
        wd = self.wd
        wd.find_element(By.LINK_TEXT, tab).click()

    def open_external_page(self, url):
        wd = self.wd
        wd.get(url)

    def destroy(self):
        self.wd.quit()
