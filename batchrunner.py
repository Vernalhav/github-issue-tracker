import argparse
import warnings
from selenium.webdriver.remote.webdriver import WebDriver
import issuehandler
from typing import Protocol, Callable
import pandas as pd

OPEN_SHEET_NAME = 'open'
CLOSE_SHEET_NAME = 'close'
COMMENT_SHEET_NAME = 'comment'

CommandLineArguments = list[str]


class BatchCommandParserArgs(Protocol):
    filename: str
    sheet_name: str
    parsing_strategy: Callable[[pd.DataFrame], list[CommandLineArguments]]


def batch_close_parser(df: pd.DataFrame) -> list[CommandLineArguments]:
    pass


def batch_open_parser(df: pd.DataFrame) -> list[CommandLineArguments]:
    pass


def batch_comment_parser(df: pd.DataFrame) -> list[CommandLineArguments]:
    pass


def batch_common_parser(df: pd.DataFrame) -> list[CommandLineArguments]:
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
    close_parser.set_defaults(
        parsing_strategy=batch_close_parser,
        sheet_name=CLOSE_SHEET_NAME)

    comment_parser = subparsers.add_parser(
        'comment', help='Add several comments, closing or reopening issues')
    comment_parser.set_defaults(
        parsing_strategy=batch_comment_parser,
        sheet_name=COMMENT_SHEET_NAME)

    open_parser = subparsers.add_parser('open', help='Opens several issues')
    open_parser.set_defaults(
        parsing_strategy=batch_open_parser,
        sheet_name=OPEN_SHEET_NAME)

    return parser


def parse_commands_from_excel(
        args: BatchCommandParserArgs) -> list[argparse.Namespace]:

    warnings.filterwarnings(
        action='ignore', category=UserWarning, module='openpyxl')

    df = pd.read_excel(args.filename, sheet_name=args.sheet_name)

    cli_options = batch_common_parser(df)
    cli_options += args.parsing_strategy(df)

    issuehandler_parser = issuehandler.create_parser()
    return [issuehandler_parser.parse_args(cli_option)
            for cli_option in cli_options]


def main():
    parser = create_parser()
    args: BatchCommandParserArgs = parser.parse_args()

    commands = parse_commands_from_excel(args)

    driver: WebDriver
    with issuehandler.get_driver() as driver:
        for command in commands:
            issuehandler.run(driver, command)


if __name__ == '__main__':
    main()
