"""Shared pytest options, fixtures, and failure evidence."""

from __future__ import annotations

import re
from collections.abc import Generator
from pathlib import Path

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from ecommerce_qa.config import Settings
from ecommerce_qa.driver_factory import create_driver
from ecommerce_qa.pages.login_page import LoginPage


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("web automation")
    group.addoption("--browser", choices=("chrome", "firefox"), help="Browser to automate")
    group.addoption("--base-url", help="Application URL")
    group.addoption("--remote-url", help="Selenium Grid URL")
    group.addoption("--headed", action="store_true", help="Show the browser window")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> Settings:
    environment = Settings.from_env()
    return environment.with_overrides(
        base_url=pytestconfig.getoption("--base-url"),
        browser=pytestconfig.getoption("--browser"),
        headless=False if pytestconfig.getoption("--headed") else None,
        remote_url=pytestconfig.getoption("--remote-url"),
    )


@pytest.fixture
def driver(settings: Settings, request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    web_driver = create_driver(settings)
    try:
        yield web_driver
    finally:
        report = getattr(request.node, "rep_call", None)
        if report and report.failed:
            safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.nodeid)
            screenshot_path = Path("screenshots") / f"{safe_name}.png"
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            png = web_driver.get_screenshot_as_png()
            screenshot_path.write_bytes(png)
            allure.attach(
                png,
                name=screenshot_path.stem,
                attachment_type=allure.attachment_type.PNG,
            )
        web_driver.quit()


@pytest.fixture
def login_page(driver: WebDriver, settings: Settings) -> LoginPage:
    return LoginPage(driver, settings).load()
