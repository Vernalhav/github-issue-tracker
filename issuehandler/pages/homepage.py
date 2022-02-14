from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from issuehandler.screenshots import SeleniumScreenshotter


class HomePage:
    URL = 'https://github.com'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    @SeleniumScreenshotter.screenshot_after(verbosity=3)
    def go(self) -> HomePage:
        self.driver.get(HomePage.URL)
        return self

    def is_logged_in(self) -> bool:
        '''
        If driver's URL is pointing to the home page,
        returns whether the user is logged in or not.
        '''
        try:
            self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Sign in')
            return False
        except NoSuchElementException:
            return True
