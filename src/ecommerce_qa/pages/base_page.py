"""Reusable browser interactions backed by explicit waits."""

from __future__ import annotations

from urllib.parse import urljoin

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ecommerce_qa.config import Settings

Locator = tuple[str, str]


class BasePage:
    """Base Page Object that keeps Selenium details out of test cases."""

    def __init__(self, driver: WebDriver, settings: Settings) -> None:
        self.driver = driver
        self.settings = settings
        self.wait = WebDriverWait(driver, settings.explicit_wait_seconds)

    def open(self, path: str = "") -> None:
        self.driver.get(urljoin(self.settings.base_url, path))

    def visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def all_visible(self, locator: Locator) -> list[WebElement]:
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator: Locator) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def click_and_wait_for_url(self, locator: Locator, fragment: str) -> None:
        """Click a React-controlled link and retry once if its first event is dropped."""

        for attempt in range(2):
            self.click(locator)
            try:
                self.wait_for_url_fragment(fragment)
                return
            except TimeoutException:
                if attempt == 1:
                    raise

    def type(self, locator: Locator, value: str) -> None:
        element = self.visible(locator)
        element.clear()
        element.send_keys(value)

    def text(self, locator: Locator) -> str:
        return self.visible(locator).text.strip()

    def wait_for_url_fragment(self, fragment: str) -> None:
        self.wait.until(EC.url_contains(fragment))

    def wait_until_absent(self, locator: Locator) -> None:
        self.wait.until(EC.invisibility_of_element_located(locator))
