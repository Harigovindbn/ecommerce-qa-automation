"""Authentication scenarios."""

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from ecommerce_qa.config import Settings
from ecommerce_qa.data.users import LOCKED_OUT_USER, STANDARD_USER
from ecommerce_qa.pages.inventory_page import InventoryPage
from ecommerce_qa.pages.login_page import LoginPage


@allure.epic("E-Commerce Web Automation")
@allure.feature("Authentication")
@allure.title("Standard user can log in")
@pytest.mark.smoke
@pytest.mark.regression
def test_standard_user_can_log_in(
    driver: WebDriver, settings: Settings, login_page: LoginPage
) -> None:
    with allure.step("Log in with the standard demo account"):
        login_page.login_as(STANDARD_USER)

    inventory = InventoryPage(driver, settings).wait_until_loaded()

    with allure.step("Verify the inventory page and product catalogue"):
        assert inventory.title() == "Products"
        assert "Sauce Labs Backpack" in inventory.product_names()


@allure.epic("E-Commerce Web Automation")
@allure.feature("Authentication")
@allure.title("Locked user is denied access")
@pytest.mark.regression
def test_locked_out_user_sees_an_error(login_page: LoginPage) -> None:
    with allure.step("Attempt login with the locked demo account"):
        login_page.login_as(LOCKED_OUT_USER)

    with allure.step("Verify the account-lock message"):
        assert "this user has been locked out" in login_page.error_message().lower()
