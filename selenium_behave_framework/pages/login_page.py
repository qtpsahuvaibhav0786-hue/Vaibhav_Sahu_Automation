"""
Login Page Object for Sauce Demo application
Demonstrates Page Object Model implementation
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Tuple

from .base_page import BasePage
from ..config.config import Config


class LoginPage(BasePage):
    """
    Page Object for Login Page
    URL: https://www.saucedemo.com
    """

    # ==================== Locators ====================
    # Using tuple format (By, locator_value) for consistency

    # Input fields
    USERNAME_INPUT: Tuple[By, str] = (By.ID, "user-name")
    PASSWORD_INPUT: Tuple[By, str] = (By.ID, "password")

    # Buttons
    LOGIN_BUTTON: Tuple[By, str] = (By.ID, "login-button")

    # Error messages
    ERROR_MESSAGE: Tuple[By, str] = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_BUTTON: Tuple[By, str] = (By.CSS_SELECTOR, ".error-button")

    # Logo
    LOGIN_LOGO: Tuple[By, str] = (By.CLASS_NAME, "login_logo")

    # ==================== Page URL ====================
    PAGE_URL = Config.BASE_URL

    def __init__(self, driver: WebDriver):
        """Initialize Login Page"""
        super().__init__(driver)
        self.logger.info("LoginPage initialized")

    # ==================== Page Actions ====================

    def open(self):
        """Open login page"""
        self.navigate_to(self.PAGE_URL)
        self.wait_for_page_load()
        self.logger.info("Opened login page")
        return self

    def enter_username(self, username: str):
        """
        Enter username

        Args:
            username: Username to enter
        """
        self.enter_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        """
        Enter password

        Args:
            password: Password to enter
        """
        self.enter_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str):
        """
        Perform login with given credentials

        Args:
            username: Username
            password: Password
        """
        self.logger.info(f"Logging in with user: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def login_as_standard_user(self):
        """Login as standard user"""
        return self.login("standard_user", "secret_sauce")

    def login_as_locked_user(self):
        """Login as locked out user"""
        return self.login("locked_out_user", "secret_sauce")

    def login_as_problem_user(self):
        """Login as problem user"""
        return self.login("problem_user", "secret_sauce")

    def login_as_performance_user(self):
        """Login as performance glitch user"""
        return self.login("performance_glitch_user", "secret_sauce")

    # ==================== Page Verifications ====================

    def is_login_page_displayed(self) -> bool:
        """Check if login page is displayed"""
        return self.is_element_visible(self.LOGIN_LOGO)

    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=3)

    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_error_displayed():
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def clear_error(self):
        """Clear error message by clicking error button"""
        if self.is_element_visible(self.ERROR_BUTTON, timeout=2):
            self.click(self.ERROR_BUTTON)
        return self

    def get_username_value(self) -> str:
        """Get current username input value"""
        return self.get_value(self.USERNAME_INPUT)

    def get_password_value(self) -> str:
        """Get current password input value"""
        return self.get_value(self.PASSWORD_INPUT)

    def is_username_field_empty(self) -> bool:
        """Check if username field is empty"""
        return self.get_username_value() == ""

    def is_password_field_empty(self) -> bool:
        """Check if password field is empty"""
        return self.get_password_value() == ""

    def clear_credentials(self):
        """Clear both username and password fields"""
        self.clear_field(self.USERNAME_INPUT)
        self.clear_field(self.PASSWORD_INPUT)
        return self

    # ==================== Page State Assertions ====================

    def verify_login_page_elements(self) -> bool:
        """Verify all login page elements are present"""
        elements_present = all([
            self.is_element_visible(self.USERNAME_INPUT),
            self.is_element_visible(self.PASSWORD_INPUT),
            self.is_element_visible(self.LOGIN_BUTTON),
            self.is_element_visible(self.LOGIN_LOGO)
        ])
        self.logger.info(f"Login page elements verification: {elements_present}")
        return elements_present

    def verify_error_message(self, expected_message: str) -> bool:
        """
        Verify error message matches expected text

        Args:
            expected_message: Expected error message

        Returns:
            True if message matches
        """
        actual_message = self.get_error_message()
        matches = expected_message in actual_message
        self.logger.info(f"Error message verification: expected='{expected_message}', actual='{actual_message}', matches={matches}")
        return matches
