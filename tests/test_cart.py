"""Shopping-cart scenarios."""

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from ecommerce_qa.config import Settings
from ecommerce_qa.data.users import STANDARD_USER
from ecommerce_qa.pages.cart_page import CartPage
from ecommerce_qa.pages.inventory_page import InventoryPage
from ecommerce_qa.pages.login_page import LoginPage

BACKPACK_SLUG = "sauce-labs-backpack"


def logged_in_inventory(
    driver: WebDriver, settings: Settings, login_page: LoginPage
) -> InventoryPage:
    login_page.login_as(STANDARD_USER)
    return InventoryPage(driver, settings).wait_until_loaded()


@allure.epic("E-Commerce Web Automation")
@allure.feature("Shopping cart")
@allure.title("User can add a product to the cart")
@pytest.mark.smoke
@pytest.mark.regression
def test_user_can_add_a_product_to_the_cart(
    driver: WebDriver, settings: Settings, login_page: LoginPage
) -> None:
    inventory = logged_in_inventory(driver, settings, login_page)

    with allure.step("Add Sauce Labs Backpack to the cart"):
        inventory.add_product(BACKPACK_SLUG)
        assert inventory.cart_count() == 1
        inventory.open_cart()

    cart = CartPage(driver, settings).wait_until_loaded()

    with allure.step("Verify the selected product in the cart"):
        assert cart.product_names() == ["Sauce Labs Backpack"]


@allure.epic("E-Commerce Web Automation")
@allure.feature("Shopping cart")
@allure.title("User can remove a product from the cart")
@pytest.mark.regression
def test_user_can_remove_a_product_from_the_cart(
    driver: WebDriver, settings: Settings, login_page: LoginPage
) -> None:
    inventory = logged_in_inventory(driver, settings, login_page)
    inventory.add_product(BACKPACK_SLUG)
    assert inventory.cart_count() == 1

    with allure.step("Remove Sauce Labs Backpack from the inventory page"):
        inventory.remove_product(BACKPACK_SLUG)
        inventory.wait_for_empty_cart()
