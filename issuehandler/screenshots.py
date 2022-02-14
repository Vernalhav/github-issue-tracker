import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Concatenate, ParamSpec, Protocol, TypeVar

from PIL import Image, ImageDraw, ImageFont
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

import issuehandler.config as config

# Return type of the decorated method
T = TypeVar('T')

# Argument types of the decorated method, excluding 'self'
# i.e. def f(self, x: int, y: str) --->  P.args = [int, str]
P = ParamSpec('P')


class PageObject(Protocol):
    driver: WebDriver


@dataclass
class Screenshot:
    path: str
    exception_occurred: bool = False
    exception_name: str = ''


class SeleniumScreenshotter:
    take_screenshots = True
    verbosity_level = 1
    output_path = Path(config.SCREENSHOTS_DIR)
    screenshots: list[Screenshot] = []

    @staticmethod
    def take_screenshot(driver: WebDriver) -> Screenshot:
        filename = f'{datetime.now().isoformat()}.png'
        filepath = str(
            SeleniumScreenshotter.output_path / filename)

        # If directory doesn't exist, create it and try again
        if not driver.save_screenshot(filepath):
            SeleniumScreenshotter.output_path.mkdir(
                parents=True, exist_ok=True)
            driver.save_screenshot(filepath)

        screenshot = Screenshot(filepath)
        SeleniumScreenshotter.screenshots.append(screenshot)
        return screenshot

    @staticmethod
    def screenshot_after(verbosity=1):
        '''
        This function should be used to decorate a method
        from a PageObject-like class (meaning it has a driver
        attribute).
        It will take a screenshot from the driver after the method
        has finished executing, and will save it to output_path.
        '''

        def _screenshot_after(
            f: Callable[Concatenate[PageObject, P], T],
        ) -> Callable[Concatenate[PageObject, P], T]:

            def wrapped_method(self: PageObject,
                               *args: P.args,
                               **kwargs: P.kwargs) -> T:

                try:
                    result = f(self, *args, **kwargs)
                    if (SeleniumScreenshotter.take_screenshots
                            and SeleniumScreenshotter.verbosity_level
                            >= verbosity):
                        SeleniumScreenshotter.take_screenshot(self.driver)
                    return result

                except WebDriverException as e:
                    image = SeleniumScreenshotter.take_screenshot(self.driver)
                    image.exception_occurred = True
                    image.exception_name = type(e).__name__
                    raise e

            return wrapped_method
        return _screenshot_after

    @staticmethod
    def save_pdf(name: str):

        if len(SeleniumScreenshotter.screenshots) == 0:
            print(f'No images in {SeleniumScreenshotter.output_path}')
            return

        Path(name).parent.mkdir(parents=True, exist_ok=True)

        first_image, *other_images = [
            _image_from_metadata(screenshot) for screenshot
            in SeleniumScreenshotter.screenshots]

        first_image.save(name, 'PDF', save_all=True,
                         append_images=other_images)

        shutil.rmtree(SeleniumScreenshotter.output_path)
        SeleniumScreenshotter.screenshots = []


def _image_from_metadata(screenshot: Screenshot) -> Image:
    image = Image.open(screenshot.path).convert('RGB')

    if screenshot.exception_occurred:
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        text_w, text_h = font.getsize(screenshot.exception_name)
        draw.rectangle((0, 0, text_w, text_h), fill='red')

    return image
