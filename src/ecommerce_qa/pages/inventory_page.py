"""Inventory Page Object."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from ecommerce_qa.pages.base_page import BasePage


class InventoryPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, '[data-test="title"]')
    PRODUCT_NAMES = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')

    def wait_until_loaded(self) -> InventoryPage:
        self.wait_for_url_fragment("inventory.html")
        self.visible(self.PAGE_TITLE)
        return self

    def title(self) -> str:
        return self.text(self.PAGE_TITLE)

    def product_names(self) -> list[str]:
        return [element.text.strip() for element in self.all_visible(self.PRODUCT_NAMES)]

    def add_product(self, product_slug: str) -> None:
        self.click((By.CSS_SELECTOR, f'[data-test="add-to-cart-{product_slug}"]'))

    def remove_product(self, product_slug: str) -> None:
        self.click((By.CSS_SELECTOR, f'[data-test="remove-{product_slug}"]'))

    def cart_count(self) -> int:
        return int(self.text(self.CART_BADGE))

    def wait_for_empty_cart(self) -> None:
        self.wait_until_absent(self.CART_BADGE)

    def open_cart(self) -> None:
        self.click_and_wait_for_url(self.CART_LINK, "cart.html")
