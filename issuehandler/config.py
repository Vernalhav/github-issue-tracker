import inspect
from pathlib import Path

module_root = Path(inspect.getframeinfo(
    inspect.currentframe()).filename).parent

DEFAULT_USER = 'Vernalhav'
DEFAULT_REPO = 'github-issue-tracker'
DRIVER_PATH = '/Users/giovannoni/selenium/drivers/chromedriver'
BROWSER_USER_PATH = str(Path(module_root, 'test-profile').resolve())
SCREENSHOTS_DIR = str(Path(module_root, 'issuehandler_screenshots').resolve())
PDF_DIR = './pdfs'
