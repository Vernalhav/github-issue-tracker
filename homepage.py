from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class HomePage:
    URL = 'https://github.com'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def go_to_page(self):
        self.driver.get(HomePage.URL)

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
    