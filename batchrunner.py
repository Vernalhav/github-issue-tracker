import argparse
import warnings
from selenium.webdriver.remote.webdriver import WebDriver
import issuehandler
from typing import Protocol, Callable
import pandas as pd

MAIN_PROGRAM_NAME = 'issuehandler.py'
OPEN_SHEET_NAME = 'open'
CLOSE_SHEET_NAME = 'close'
COMMENT_SHEET_NAME = 'comment'

CommandLineArguments = list[str | int]


class MissingRequiredFieldException(Exception):
    field: str
    row: str
    sheet_name: str
    file_name: str

    def __init__(self, field: str, row=-1, sheet_name='', file_name=''):
        self.field = field
        self.row = row
        self.sheet_name = sheet_name
        self.file_name = file_name
        super().__init__(
            f'{file_name} in sheet {sheet_name}: '
            + f'missing required field {field} at row {row}')


class BatchCommandParserArgs(Protocol):
    filename: str
    sheet_name: str
    parsing_strategy: Callable[[pd.Series], CommandLineArguments]


def batch_close_parser(row: pd.Series) -> CommandLineArguments:
    cli_options = ['close']

    if row.isna()['Issue ID']:
        raise MissingRequiredFieldException('Issue ID')

    cli_options.append(row['Issue ID'])
    return cli_options


def batch_open_parser(row: pd.Series) -> CommandLineArguments:
    cli_options = ['open']

    if row.isna()['Title'] or len(row['Title']) == 0:
        raise MissingRequiredFieldException('Title')

    cli_options += ['--title', row['Title']]

    if not row.isna()['Body'] and len(row['Body']) > 0:
        cli_options += ['--body', row['Body']]

    return cli_options


def batch_comment_parser(row: pd.Series) -> CommandLineArguments:
    cli_options = ['comment']

    if row.isna()['Issue ID']:
        raise MissingRequiredFieldException('Issue ID')

    cli_options.append(row['Issue ID'])

    if row.isna()['Comment'] or len(row['Comment']) == 0:
        raise MissingRequiredFieldException('Comment')

    cli_options += ['--message', row['Comment']]

    if not row.isna()['Action'] and len(row['Action']) > 0:
        actions = {'Close': '--close', 'Reopen': '--reopen'}
        cli_options.append(actions[row['Action']])

    return cli_options


def batch_common_parser(row: pd.Series) -> CommandLineArguments:
    cli_options = []

    if not row.isna()['Repo owner']:
        cli_options += ['--user', row['Repo owner']]

    if not row.isna()['Repo name']:
        cli_options += ['--repo', row['Repo name']]

    if not row.isna()['Verbosity'] and row['Verbosity'] > 0:
        cli_options += ['--pdf', '--verbosity', int(row['Verbosity'])]

    return cli_options


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

    commands = []
    for row_id, row in df.iterrows():
        try:
            cli_options = batch_common_parser(row)
            cli_options += args.parsing_strategy(row)
            commands.append([str(option) for option in cli_options])

        except MissingRequiredFieldException as e:
            raise MissingRequiredFieldException(
                field=e.field,
                row=str(row_id),
                sheet_name=args.sheet_name,
                file_name=args.filename)

    issuehandler_parser = issuehandler.create_parser()
    return [issuehandler_parser.parse_args(command)
            for command in commands]


def main():
    parser = create_parser()
    args: BatchCommandParserArgs = parser.parse_args()

    commands = parse_commands_from_excel(args)

    driver: WebDriver
    with issuehandler.get_driver() as driver:
        for command in commands:
            issuehandler.run(driver, command)
            driver.switch_to.new_window('tab')


if __name__ == '__main__':
    main()
