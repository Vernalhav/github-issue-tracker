from __future__ import annotations
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from issuepage import IssuePage
from newissuepage import NewIssuePage
from screenshots import SeleniumScreenshotter


class NoIssueWithIDException(Exception):
    pass


class IssuesPage:
    def __init__(self, driver: WebDriver, repo_url: str):
        self.driver = driver
        self.url = f'{repo_url}/issues'

    @SeleniumScreenshotter.screenshot_after(verbosity=2)
    def go(self) -> IssuesPage:
        self.driver.get(self.url)
        self.find_elements()
        return self

    def find_elements(self):
        self.issue_search_box = self.driver.find_element(
            By.ID, 'js-issues-search')

    def get_new_issue_page(self) -> NewIssuePage:
        return NewIssuePage(self.driver, self.url)

    @SeleniumScreenshotter.screenshot_after()
    def get_issue_by_id(self, id: int) -> IssuePage:
        self.issue_search_box.clear()
        self.issue_search_box.send_keys(Keys.RETURN)

        try:
            self.driver.find_element(By.ID, f'issue_{id}_link')
            return IssuePage(self.driver, id, f'{self.url}/{id}')
        except NoSuchElementException:
            raise NoIssueWithIDException(
                f'Could not find issue with id {id} on page {self.url}')
