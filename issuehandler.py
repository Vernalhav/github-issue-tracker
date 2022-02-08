import config
from selenium import webdriver
from issuespage import IssuesPage
from loginpage import LoginPage
from repopage import RepoPage
from selenium.webdriver.chrome.service import Service


def get_driver():
    service = Service(config.DRIVER_PATH)
    options = webdriver.ChromeOptions()

    options.add_argument(f"--user-data-dir={config.BROWSER_USER_PATH}")
    driver = webdriver.Chrome(options=options, service=service)
    return driver


def main():
    repo_url = 'https://github.com/Vernalhav/github-issue-tracker'

    with get_driver() as driver:
        login_page = LoginPage(driver)
        print(login_page.is_logged_in())


if __name__ == '__main__':
    main()