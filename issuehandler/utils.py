from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver, WebElement


def safe_send_keys(driver: WebDriver, textbox: WebElement, text: str):
    textbox.click()
    action = ActionChains(driver)
    action.send_keys(text)
    action.perform()


def switch_tab_and_close_previous(driver: WebDriver):
    previous_tab = driver.current_window_handle
    driver.switch_to.new_window('tab')
    new_tab = driver.current_window_handle
    driver.switch_to.window(previous_tab)
    driver.close()
    driver.switch_to.window(new_tab)
