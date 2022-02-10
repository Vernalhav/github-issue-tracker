from selenium.webdriver.remote.webdriver import WebDriver
from typing import Concatenate, Protocol, Callable, TypeVar, ParamSpec
from pathlib import Path

# Return type of the decorated method
T = TypeVar('T')

# Argument types of the decorated method, excluding 'self'
# i.e. def f(self, x: int, y: str) --->  P.args = [int, str]
P = ParamSpec('P')


class PageObject(Protocol):
    driver: WebDriver


class SeleniumScreenshotter:
    take_screenshots = False
    output_path = Path('./')

    @staticmethod
    def screenshot_after(
        f: Callable[Concatenate[PageObject, P], T]
    ) -> Callable[Concatenate[PageObject, P], T]:

        def wrapped_method(self: PageObject,
                           *args: P.args,
                           **kwargs: P.kwargs) -> T:

            result = f(self, *args, **kwargs)
            if SeleniumScreenshotter.take_screenshots:
                self.driver.save_screenshot()
            return result

        return wrapped_method
