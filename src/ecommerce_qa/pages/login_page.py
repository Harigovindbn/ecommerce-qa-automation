"""Login Page Object."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from ecommerce_qa.data.users import User
from ecommerce_qa.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.CSS_SELECTOR, '[data-test="username"]')
    PASSWORD = (By.CSS_SELECTOR, '[data-test="password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-test="login-button"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')

    def load(self) -> LoginPage:
        self.open()
        self.visible(self.LOGIN_BUTTON)
        return self

    def login_as(self, user: User) -> None:
        self.type(self.USERNAME, user.username)
        self.type(self.PASSWORD, user.password)
        self.click(self.LOGIN_BUTTON)

    def error_message(self) -> str:
        return self.text(self.ERROR_MESSAGE)
