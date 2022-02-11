import argparse
from selenium.webdriver.remote.webdriver import WebDriver
import issuehandler
from typing import Protocol, Callable


class BatchCommandParserArgs(Protocol):
    filename: str
    parsing_strategy: Callable[[str], list[argparse.Namespace]]


def batch_close_parser(filename: str) -> list[argparse.Namespace]:
    pass


def batch_open_parser(filename: str) -> list[argparse.Namespace]:
    pass


def batch_comment_parser(filename: str) -> list[argparse.Namespace]:
    pass


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file',
        help='Name of the batch file',
        type=str, required=True,
        dest='filename')

    subparsers = parser.add_subparsers(required=True, title='Operation')

    close_parser = subparsers.add_parser('close', help='Closes several issues')
    close_parser.set_defaults(parsing_strategy=batch_close_parser)

    comment_parser = subparsers.add_parser(
        'comment', help='Add several comments, closing or reopening issues')
    comment_parser.set_defaults(parsing_strategy=batch_comment_parser)

    open_parser = subparsers.add_parser('open', help='Opens several issues')
    open_parser.set_defaults(parsing_strategy=batch_open_parser)

    return parser


def main():
    parser = create_parser()
    args: BatchCommandParserArgs = parser.parse_args()

    commands = args.parsing_strategy(args.filename)

    driver: WebDriver
    with issuehandler.get_driver() as driver:
        for command in commands:
            issuehandler.run(driver, command)


if __name__ == '__main__':
    main()
