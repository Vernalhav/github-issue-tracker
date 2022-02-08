from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = 'https://github.com/login'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def wait_for_manual_login(self):
        WebDriverWait(self.driver, 30).until(EC.url_to_be())

    