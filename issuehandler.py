import config
from selenium import webdriver
from homepage import HomePage
from issuespage import NoIssueWithIDException
from loginpage import LoginPage
from repopage import RepoPage
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
import argparse


def get_driver() -> WebDriver:
    service = Service(config.DRIVER_PATH)

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={config.BROWSER_USER_PATH}")

    driver = webdriver.Chrome(options=options, service=service)
    driver.implicitly_wait(0.5)
    return driver


def login_manually(driver: WebDriver) -> bool:
    login_page = LoginPage(driver).go()

    try:
        login_page.wait_for_manual_login()
        return True
    except TimeoutException:
        return False


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--user', help='Name of the owner of the repo',
        default=config.DEFAULT_USER)
    parser.add_argument(
        '--repo', help='Name of the GitHub repository',
        default=config.DEFAULT_REPO)
    subparsers = parser.add_subparsers(required=True, title='Operation')

    parser_close = subparsers.add_parser('close', help='Closes an issue')
    parser_close.add_argument(
        'id', type=int, help='GitHub ID of the issue to be closed')
    parser_close.set_defaults(function=close_issue)

    parser_comment = subparsers.add_parser(
        'comment', help='Add comment to issue')
    parser_comment.add_argument(
        'id', type=int, help='GitHub ID of the issue')
    parser_comment.add_argument(
        '-m', '--message',
        type=str, help='Quote-delimited comment to add',
        required=True)
    parser_comment.add_argument(
        '-c', '--close', help='Set this to close the issue with the comment',
        action='store_true')
    parser_comment.set_defaults(function=comment_issue)

    return parser


def close_issue(repo_url: str, id: int, **kwargs):
    with get_driver() as driver:
        home_page = HomePage(driver).go()

        if not home_page.is_logged_in() and not login_manually(driver):
            print('User has not logged in')
            return

        repo_page = RepoPage(driver, repo_url).go()
        issues_page = repo_page.go_to_issues().go()

        try:
            issue = issues_page.get_issue_by_id(id).go()

            if not issue.is_open:
                print('Issue is already closed')
                return

            issue.close()

        except NoIssueWithIDException:
            print('No issue found with specified ID')


def comment_issue(repo_url: str, id: int, message: str, close: bool, **kwargs):
    with get_driver() as driver:
        home_page = HomePage(driver).go()

        if not home_page.is_logged_in() and not login_manually(driver):
            print('User has not logged in')
            return

        repo_page = RepoPage(driver, repo_url).go()
        issues_page = repo_page.go_to_issues().go()

        try:
            issue = issues_page.get_issue_by_id(id).go()
            issue.comment(message, close)

        except NoIssueWithIDException:
            print('No issue found with specified ID')


def main():
    arg_parser = create_parser()
    args = arg_parser.parse_args()

    SITE_URL = 'https://www.github.com'
    args.repo_url = f'{SITE_URL}/{config.DEFAULT_USER}/{config.DEFAULT_REPO}'
    args.function(**vars(args))


if __name__ == '__main__':
    main()
