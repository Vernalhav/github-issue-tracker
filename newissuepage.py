from __future__ import annotations
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import _safe_send_keys


class NewIssuePage:
    def __init__(self, driver: WebDriver, issues_page_url: str):
        self.driver = driver
        self.url = f'{issues_page_url}/new'

    def go(self) -> NewIssuePage:
        self.driver.get(self.url)
        self.find_elements()
        return self

    def find_elements(self):
        self.issue_title_bpx = self.driver.find_element(
            By.ID, 'issue_title')
        self.issue_body_box = self.driver.find_element(By.ID, 'issue_body')
        self.new_issue_button = self.driver.find_element(
            By.XPATH, '//button[normalize-space()="Submit new issue"]')

    def open_new_issue(self, title: str, body: str):
        self.issue_body_box.clear()
        self.issue_title_bpx.clear()
        _safe_send_keys(self.driver, self.issue_title_bpx, title)
        _safe_send_keys(self.driver, self.issue_body_box, body)

        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.new_issue_button))
        self.new_issue_button.click()
