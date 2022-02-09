from __future__ import annotations
from selenium.webdriver.remote.webdriver import WebDriver
from utils import _safe_send_keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import NoSuchElementException


class IssuePage:
    def __init__(self, driver: WebDriver, id: int, url: str):
        self.driver = driver
        self.id = id
        self.url = url

    def go(self) -> IssuePage:
        self.driver.get(self.url)
        self._find_elements()
        return self

    def close(self):
        self.update_status()
        if self.is_open:
            self.close_button.click()

    def reopen(self):
        self.update_status()
        if not self.is_open:
            self.reopen_button.click()

    def comment(self, comment: str, close=False, reopen=False):
        self.update_status()

        self.comment_box.clear()
        _safe_send_keys(self.driver, self.comment_box, comment)

        if close:
            self.close()
        elif reopen:
            self.reopen()
        else:
            self.comment_button.click()

    def update_status(self):
        self._find_elements()

    def _is_open(self) -> bool:
        try:
            self.driver.find_element(
                By.CSS_SELECTOR, '[title="Status: Closed"]')
            return False
        except NoSuchElementException:
            return True

    def _find_elements(self):
        self.is_open = self._is_open()

        self.close_button = None
        self.reopen_button = None

        if self.is_open:
            self.close_button = self.driver.find_element(
                By.NAME, 'comment_and_close')
        else:
            self.reopen_button = self.driver.find_element(
                By.NAME, 'comment_and_open')

        self.comment_box = self.driver.find_element(By.ID, 'new_comment_field')
        self.comment_button = self.driver.find_element(locate_with(
            By.TAG_NAME, 'button').to_right_of(
                self.close_button or self.reopen_button))
