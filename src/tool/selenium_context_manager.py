"""
This is Selenium context manager!
"""
from selenium import webdriver


selenium_url : str = "src/tool/chromedriver"


class SeleniumContextManager:
    """
    Title : SeleniumContextManager
    This class is to deal selenium with context manager!
    selenium should close connection!
    Because it exist in memory even if it's over
    Attributes:
        - __init__ : Setting selenium!
        - __enter__ : return connection!
        - __exit__ : quit connection!
    """
    def __init__(self):

        options = webdriver.ChromeOptions()

        options.add_argument('headless')

        options.add_argument('window-size=1920x1080')

        options.add_argument("disable-gpu")

        options.add_argument('--no-sandbox')

        options.add_argument("--single-process")

        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(selenium_url, chrome_options=options)

        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()