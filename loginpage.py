from __future__ import annotations
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from homepage import HomePage


class LoginPage:
    URL = 'https://www.github.com/login'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def go(self) -> LoginPage:
        self.driver.get(LoginPage.URL)
        return self

    def wait_for_manual_login(self):
        WebDriverWait(self.driver, 20).until(EC.url_to_be(HomePage.URL + '/'))
