from selenium.webdriver.remote.webdriver import WebDriver

from issuespage import IssuesPage

class RepoPage:
    def __init__(self, driver: WebDriver, repo_url: str):
        self.driver = driver
        self.repo_url = repo_url

        self.issues_anchor = driver.find_element_by_id('issues-tab')

    @staticmethod
    def go_to_repo(repo_url: str, driver: WebDriver):
        driver.get(repo_url)
        return RepoPage(driver, repo_url)

    def go_to_issues(self) -> IssuesPage:
        self.issues_anchor.click()
        return IssuesPage(self.driver)