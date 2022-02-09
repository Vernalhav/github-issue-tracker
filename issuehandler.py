import config
from selenium import webdriver
from homepage import HomePage
from loginpage import LoginPage
from repopage import RepoPage
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException


def get_driver() -> WebDriver:
    service = Service(config.DRIVER_PATH)

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={config.BROWSER_USER_PATH}")

    driver = webdriver.Chrome(options=options, service=service)
    return driver


def login_manually(driver: WebDriver) -> bool:
    login_page = LoginPage(driver).go()

    try:
        login_page.wait_for_manual_login()
        return True
    except TimeoutException:
        return False


def main():
    repo_url = 'https://www.github.com/Vernalhav/github-issue-tracker'

    with get_driver() as driver:
        home_page = HomePage(driver).go()

        if not home_page.is_logged_in() and not login_manually(driver):
            print('User has not logged in')
            return

        repo_page = RepoPage(driver, repo_url).go()
        issues_page = repo_page.go_to_issues().go()
        issue = issues_page.get_issue_by_id(1).go()
        issue.comment('wow this is cool')


if __name__ == '__main__':
    main()
