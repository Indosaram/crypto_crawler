import os
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium_helper.selenium_loader import SeleniumLoader

SeleniumLoader()


class SeleniumBase:
    """
    Base class for handy selenium usage.
    """

    def __init__(self):
        # TODO: Add user custom option
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": os.path.join(
                    os.getcwd(), "images"
                ),
                "download.prompt_for_download": False,
                'profile.default_content_setting_values.automatic_downloads': False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False,
            },
        )
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        )
        options.add_argument('lang=ko_KR')
        options.add_argument('log-level=3')  # To ignore message

        self.driver = webdriver.Chrome(
            os.path.join(os.getcwd(), "chromedriver"), options=options
        )

    def click(self, xpath: str):
        """
        Wrapper function of clicking DOM element
        """
        self.wait_until(xpath)
        element = self.driver.find_element_by_xpath(xpath)
        self._click(element)

    def _click(self, element: WebElement):
        webdriver.ActionChains(self.driver).move_to_element(element).click(
            element
        ).perform()

    def click_and_send_key(self, xpath: str, key: str):
        self.wait_until(xpath)
        element = self.driver.find_element_by_xpath(xpath)
        self._click(element)
        element.send_keys(key)

    def __del__(self):
        self.driver.close()

    def wait_until(
        self, xpath: str, wait_time: int = 3
    ) -> Optional[WebElement]:
        element = WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element

    def scroll_down(self, height: Optional[int] = None, bottom: bool = True):
        """
        Wrapper function for scrolling down the page. It will goes to the bottom
        of the page by default.
        """
        if bottom:
            height = "document.body.scrollHeight"
            if height is not None:
                print("'height' parameter is ignored due to 'bottom' parameter")

        self.driver.execute_script(f"window.scrollTo(0, {height});")
