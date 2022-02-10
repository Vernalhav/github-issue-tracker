from __future__ import annotations
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from issuespage import IssuesPage
from screenshots import SeleniumScreenshotter


class RepoPage:
    def __init__(self, driver: WebDriver, repo_url: str):
        self.driver = driver
        self.repo_url = repo_url

    @SeleniumScreenshotter.screenshot_after(verbosity=2)
    def go(self) -> RepoPage:
        self.driver.get(self.repo_url)
        self.find_elements()
        return self

    def find_elements(self):
        self.issues_anchor = self.driver.find_element(By.ID, 'issues-tab')

    def go_to_issues(self) -> IssuesPage:
        self.issues_anchor.click()
        return IssuesPage(self.driver, self.repo_url)
