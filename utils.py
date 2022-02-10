from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver, WebElement


def safe_send_keys(driver: WebDriver, textbox: WebElement, text: str):
    textbox.click()
    action = ActionChains(driver)
    action.send_keys(text)
    action.perform()
