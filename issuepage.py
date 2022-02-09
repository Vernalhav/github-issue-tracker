from __future__ import annotations
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with


class IssuePage:
    def __init__(self, driver: WebDriver, id: int, url: str):
        self.driver = driver
        self.id = id
        self.url = url

    def go(self) -> IssuePage:
        self.driver.get(self.url)
        self.find_elements()
        return self

    def find_elements(self):
        self.comment_box = self.driver.find_element(By.ID, 'new_comment_field')
        self.close_button = self.driver.find_element(
            By.NAME, 'comment_and_close')
        self.comment_button = self.driver.find_element(locate_with(
            By.TAG_NAME, 'button').to_right_of(self.close_button))

    def close(self):
        self.close_button.click()

    def comment(self, comment: str, close=False):
        self.comment_box.clear()
        self._safe_send_keys(self.comment_box, comment)

        if close:
            self.close()
        else:
            self.comment_button.click()

    def _safe_send_keys(self, textbox: WebElement, text: str):
        textbox.click()
        action = ActionChains(self.driver)
        action.send_keys(text)
        action.perform()
