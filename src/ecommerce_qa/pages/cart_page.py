"""Shopping Cart Page Object."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from ecommerce_qa.pages.base_page import BasePage


class CartPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    PRODUCT_NAMES = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, '[data-test="checkout"]')

    def wait_until_loaded(self) -> CartPage:
        self.wait_for_url_fragment("cart.html")
        self.visible(self.PAGE_TITLE)
        return self

    def product_names(self) -> list[str]:
        return [element.text.strip() for element in self.all_visible(self.PRODUCT_NAMES)]

    def begin_checkout(self) -> None:
        self.click_and_wait_for_url(self.CHECKOUT_BUTTON, "checkout-step-one.html")
