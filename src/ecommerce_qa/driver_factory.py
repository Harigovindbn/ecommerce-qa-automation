"""WebDriver creation for local browsers and Selenium Grid."""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from ecommerce_qa.config import Settings


def _chrome_options(headless: bool) -> ChromeOptions:
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    return options


def _firefox_options(headless: bool) -> FirefoxOptions:
    options = FirefoxOptions()
    if headless:
        options.add_argument("-headless")
    options.add_argument("--width=1440")
    options.add_argument("--height=900")
    return options


def create_driver(settings: Settings) -> WebDriver:
    options = (
        _chrome_options(settings.headless)
        if settings.browser == "chrome"
        else _firefox_options(settings.headless)
    )

    if settings.remote_url:
        driver = webdriver.Remote(command_executor=settings.remote_url, options=options)
    elif settings.browser == "chrome":
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Firefox(options=options)

    driver.set_page_load_timeout(30)
    driver.set_window_size(1440, 900)
    return driver
