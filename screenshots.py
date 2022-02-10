import shutil
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Concatenate, Protocol, Callable, TypeVar, ParamSpec
from pathlib import Path
from datetime import datetime
import glob
from PIL import Image
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

        def wrapped_method(self: PageObject,
                           *args: P.args,
                           **kwargs: P.kwargs) -> T:

            result = f(self, *args, **kwargs)
            if SeleniumScreenshotter.take_screenshots:
                filename = f'{datetime.now().isoformat()}.png'
                filepath = str(SeleniumScreenshotter.output_path / filename)

                # If directory doesn't exist, create it and try again
                if not self.driver.save_screenshot(filepath):
                    SeleniumScreenshotter.output_path.mkdir(
                        parents=True, exist_ok=True)
                    self.driver.save_screenshot(filepath)

            return result

        return wrapped_method

    @staticmethod
    def save_pdf(name: str):
        image_paths = sorted(glob.glob(
            f'{SeleniumScreenshotter.output_path}/*.png'))

        if len(image_paths) == 0:
            print(f'No images in {SeleniumScreenshotter.output_path}')
            return

        first_image, *other_images = [Image.open(image_path).convert('RGB')
                                      for image_path in image_paths]

        Path(name).parent.mkdir(parents=True, exist_ok=True)
        first_image.save(name, 'PDF', save_all=True,
                         append_images=other_images)

        shutil.rmtree(SeleniumScreenshotter.output_path)
