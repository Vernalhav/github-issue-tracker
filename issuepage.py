from __future__ import annotations
from selenium.webdriver.remote.webdriver import WebDriver


class IssuePage:
    def __init__(self, driver: WebDriver, id: int, url: str):
        self.driver = driver
        self.id = id
        self.url = url

    def go(self) -> IssuePage:
        self.driver.get(self.url)
        return self

    def close(self):
        pass

    def comment(self, comment: str):
        pass
