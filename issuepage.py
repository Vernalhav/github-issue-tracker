from selenium.webdriver.remote.webdriver import WebDriver


class IssuePage:
    def __init__(self, driver: WebDriver, id: int, url: str):
        self.driver = driver
        self.id = id
        self.url = url

    def go_to_page(self):
        self.driver.get(self.url)

    def close(self):
        pass

    def comment(self, comment: str):
        pass
