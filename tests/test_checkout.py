"""End-to-end checkout scenario."""

import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from ecommerce_qa.config import Settings
from ecommerce_qa.data.users import STANDARD_USER
from ecommerce_qa.pages.cart_page import CartPage
from ecommerce_qa.pages.checkout_page import CheckoutPage
from ecommerce_qa.pages.inventory_page import InventoryPage
from ecommerce_qa.pages.login_page import LoginPage


@allure.epic("E-Commerce Web Automation")
@allure.feature("Checkout")
@allure.title("User can complete an order")
@pytest.mark.regression
@pytest.mark.e2e
def test_user_can_complete_checkout(
    driver: WebDriver, settings: Settings, login_page: LoginPage
) -> None:
    login_page.login_as(STANDARD_USER)
    inventory = InventoryPage(driver, settings).wait_until_loaded()
    inventory.add_product("sauce-labs-backpack")
    inventory.open_cart()

    cart = CartPage(driver, settings).wait_until_loaded()
    cart.begin_checkout()

    checkout = CheckoutPage(driver, settings)
    with allure.step("Submit customer information"):
        checkout.enter_customer_information(
            first_name="Hari",
            last_name="Nair",
            postal_code="50000",
        )

    with allure.step("Finish the order and verify confirmation"):
        checkout.finish_order()
        assert checkout.completion_message() == "Thank you for your order!"
