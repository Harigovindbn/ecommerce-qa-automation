"""Checkout Page Object."""

from selenium.webdriver.common.by import By

from ecommerce_qa.pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, '[data-test="firstName"]')
    LAST_NAME = (By.CSS_SELECTOR, '[data-test="lastName"]')
    POSTAL_CODE = (By.CSS_SELECTOR, '[data-test="postalCode"]')
    CONTINUE_BUTTON = (By.CSS_SELECTOR, '[data-test="continue"]')
    FINISH_BUTTON = (By.CSS_SELECTOR, '[data-test="finish"]')
    COMPLETE_HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')

    def enter_customer_information(
        self, *, first_name: str, last_name: str, postal_code: str
    ) -> None:
        self.wait_for_url_fragment("checkout-step-one.html")
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        self.click_and_wait_for_url(self.CONTINUE_BUTTON, "checkout-step-two.html")

    def finish_order(self) -> None:
        self.click_and_wait_for_url(self.FINISH_BUTTON, "checkout-complete.html")

    def completion_message(self) -> str:
        return self.text(self.COMPLETE_HEADER)
