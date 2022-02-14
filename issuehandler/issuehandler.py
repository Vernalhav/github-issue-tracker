import argparse
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver

import issuehandler.config as config
from issuehandler.pages import (HomePage, LoginPage, NoIssueWithIDException,
                                RepoPage)
from issuehandler.screenshots import SeleniumScreenshotter


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
    parser.add_argument(
        '--pdf', help='Whether to generate a PDF file with screenshots',
        action='store_true', dest='take_screenshots')
    parser.add_argument('-v', '--verbosity',
                        help='Set screenshot verbosity level',
                        type=int, choices=[1, 2, 3], default=3)
    subparsers = parser.add_subparsers(required=True, title='Operation')

    close_parser = subparsers.add_parser('close', help='Closes an issue')
    close_parser.add_argument(
        'id', type=int, help='GitHub ID of the issue to be closed')
    close_parser.set_defaults(function=close_issue)

    comment_parser = subparsers.add_parser(
        'comment', help='Adds comment to issue')
    comment_parser.add_argument(
        'id', type=int, help='GitHub ID of the issue')
    comment_parser.add_argument(
        '-m', '--message',
        type=str, help='Quote-delimited comment to add',
        required=True)
    group = comment_parser.add_mutually_exclusive_group()
    group.add_argument(
        '-c', '--close', help='Set this to close the issue with acomment',
        action='store_true')
    group.add_argument(
        '-o', '--reopen',
        help='Set this to reopen the closed issue with a comment',
        action='store_true')
    comment_parser.set_defaults(function=comment_issue)

    open_parser = subparsers.add_parser('open', help='Opens a new issue')
    open_parser.add_argument('--title', type=str, required=True)
    open_parser.add_argument('--body', type=str, default='')
    open_parser.set_defaults(function=open_issue)

    return parser


def open_issue(repo_url: str, title: str,
               body: str, driver: WebDriver,
               **kwargs):

    repo_page = RepoPage(driver, repo_url).go()
    issues_page = repo_page.go_to_issues().go()
    new_issue_page = issues_page.get_new_issue_page().go()
    new_issue_page.open_new_issue(title, body)


def close_issue(repo_url: str, id: int, driver: WebDriver, **kwargs):
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


def comment_issue(repo_url: str, id: int,
                  message: str, close: bool,
                  reopen: bool, driver: WebDriver,
                  **kwargs):

    repo_page = RepoPage(driver, repo_url).go()
    issues_page = repo_page.go_to_issues().go()

    try:
        issue = issues_page.get_issue_by_id(id).go()
        issue.comment(message, close, reopen)

    except NoIssueWithIDException:
        print('No issue found with specified ID')


def run(driver: WebDriver, args: argparse.Namespace):
    SeleniumScreenshotter.take_screenshots = args.take_screenshots
    SeleniumScreenshotter.verbosity_level = args.verbosity

    SITE_URL = 'https://www.github.com'
    args.repo_url = f'{SITE_URL}/{args.user}/{args.repo}'
    args.driver = driver

    home_page = HomePage(driver).go()

    if not home_page.is_logged_in() and not login_manually(driver):
        print('User has not logged in')
        return

    args.function(**vars(args))

    if args.take_screenshots:
        pdf_name = datetime.now().strftime('%Y-%m-%dT%Hh%Mm%Ss')
        SeleniumScreenshotter.save_pdf(f'{config.PDF_DIR}/{pdf_name}.pdf')


def main():
    arg_parser = create_parser()
    args = arg_parser.parse_args()

    driver: WebDriver
    with get_driver() as driver:
        run(driver, args)


if __name__ == '__main__':
    main()
