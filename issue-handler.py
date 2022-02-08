from selenium import webdriver


def main():
    driver = webdriver.Safari()
    driver.get('https://google.com')
    driver.quit()


if __name__ == '__main__':
    main()