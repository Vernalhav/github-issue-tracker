from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    LOGIN_URL = 'https://github.com/login'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def is_logged_in(self) -> bool:
        self.driver.get(LoginPage.LOGIN_URL)
        return 'login' not in self.driver.current_url
    