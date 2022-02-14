from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from issuehandler.screenshots import SeleniumScreenshotter

from .homepage import HomePage


class LoginPage:
    URL = 'https://www.github.com/login'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    @SeleniumScreenshotter.screenshot_after(verbosity=3)
    def go(self) -> LoginPage:
        self.driver.get(LoginPage.URL)
        return self

    @SeleniumScreenshotter.screenshot_after(verbosity=3)
    def wait_for_manual_login(self):
        WebDriverWait(self.driver, 60).until(EC.url_to_be(HomePage.URL + '/'))
