import time
import config
from selenium import webdriver
from homepage import HomePage
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
    repo_url = 'https://www.github.com/Vernalhav/github-issue-tracker'

    with get_driver() as driver:
        home_page = HomePage(driver)
        home_page.go_to_page()
        
        if not home_page.is_logged_in():
            login_page = LoginPage(driver)
            login_page.go_to_page()
            login_page.wait_for_manual_login()

        print(f'End')

if __name__ == '__main__':
    main()