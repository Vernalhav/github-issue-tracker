from selenium.webdriver.remote.webdriver import WebDriver
from typing import Concatenate, Protocol, Callable, TypeVar, ParamSpec
from pathlib import Path
from datetime import datetime
import config

# Return type of the decorated method
T = TypeVar('T')

# Argument types of the decorated method, excluding 'self'
# i.e. def f(self, x: int, y: str) --->  P.args = [int, str]
P = ParamSpec('P')


class PageObject(Protocol):
    driver: WebDriver


class SeleniumScreenshotter:
    take_screenshots = True
    output_path = Path(config.SCREENSHOTS_DIR)

    @staticmethod
    def screenshot_after(
        f: Callable[Concatenate[PageObject, P], T]
    ) -> Callable[Concatenate[PageObject, P], T]:
        '''
        This function should be used to decorate a method
        from a PageObject-like class (meaning it has a driver
        attribute).
        It will take a screenshot from the driver after the method
        has finished executing, and will save it to output_path.
        '''

        SeleniumScreenshotter.output_path.mkdir(parents=True, exist_ok=True)

        def wrapped_method(self: PageObject,
                           *args: P.args,
                           **kwargs: P.kwargs) -> T:

            result = f(self, *args, **kwargs)
            if SeleniumScreenshotter.take_screenshots:
                filename = f'{datetime.now().isoformat()}.png'
                filepath = str(SeleniumScreenshotter.output_path / filename)

                self.driver.save_screenshot(filepath)
            return result

        return wrapped_method

    @staticmethod
    def save_pdf():
        pass
