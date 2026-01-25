"""
Checkout Page Objects for Sauce Demo application
Represents checkout step one, step two, and complete pages
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Tuple, List, Dict

from .base_page import BasePage


class CheckoutStepOnePage(BasePage):
    """
    Page Object for Checkout Step One (Your Information)
    URL: https://www.saucedemo.com/checkout-step-one.html
    """

    # ==================== Locators ====================

    TITLE: Tuple[By, str] = (By.CLASS_NAME, "title")

    # Input fields
    FIRST_NAME_INPUT: Tuple[By, str] = (By.ID, "first-name")
    LAST_NAME_INPUT: Tuple[By, str] = (By.ID, "last-name")
    POSTAL_CODE_INPUT: Tuple[By, str] = (By.ID, "postal-code")

    # Buttons
    CANCEL_BUTTON: Tuple[By, str] = (By.ID, "cancel")
    CONTINUE_BUTTON: Tuple[By, str] = (By.ID, "continue")

    # Error message
    ERROR_MESSAGE: Tuple[By, str] = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_BUTTON: Tuple[By, str] = (By.CSS_SELECTOR, ".error-button")

    def __init__(self, driver: WebDriver):
        """Initialize Checkout Step One Page"""
        super().__init__(driver)
        self.logger.info("CheckoutStepOnePage initialized")

    # ==================== Page Actions ====================

    def enter_first_name(self, first_name: str):
        """Enter first name"""
        self.enter_text(self.FIRST_NAME_INPUT, first_name)
        return self

    def enter_last_name(self, last_name: str):
        """Enter last name"""
        self.enter_text(self.LAST_NAME_INPUT, last_name)
        return self

    def enter_postal_code(self, postal_code: str):
        """Enter postal code"""
        self.enter_text(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def fill_information(self, first_name: str, last_name: str, postal_code: str):
        """
        Fill all checkout information

        Args:
            first_name: First name
            last_name: Last name
            postal_code: Postal/ZIP code
        """
        self.logger.info(f"Filling checkout info: {first_name} {last_name}, {postal_code}")
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self

    def click_continue(self):
        """Click Continue button"""
        self.click(self.CONTINUE_BUTTON)
        return self

    def click_cancel(self):
        """Click Cancel button"""
        self.click(self.CANCEL_BUTTON)
        return self

    def proceed_with_info(self, first_name: str, last_name: str, postal_code: str):
        """Fill info and continue"""
        self.fill_information(first_name, last_name, postal_code)
        self.click_continue()
        return self

    # ==================== Page Verifications ====================

    def is_checkout_step_one_displayed(self) -> bool:
        """Check if checkout step one page is displayed"""
        return self.is_element_visible(self.FIRST_NAME_INPUT)

    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=3)

    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_error_displayed():
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def verify_error_message(self, expected_message: str) -> bool:
        """Verify error message contains expected text"""
        actual_message = self.get_error_message()
        return expected_message in actual_message


class CheckoutStepTwoPage(BasePage):
    """
    Page Object for Checkout Step Two (Overview)
    URL: https://www.saucedemo.com/checkout-step-two.html
    """

    # ==================== Locators ====================

    TITLE: Tuple[By, str] = (By.CLASS_NAME, "title")

    # Cart items
    CART_ITEMS: Tuple[By, str] = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES: Tuple[By, str] = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES: Tuple[By, str] = (By.CLASS_NAME, "inventory_item_price")

    # Summary
    PAYMENT_INFO_LABEL: Tuple[By, str] = (By.CSS_SELECTOR, ".summary_info_label:nth-of-type(1)")
    PAYMENT_INFO_VALUE: Tuple[By, str] = (By.CSS_SELECTOR, ".summary_value_label:nth-of-type(1)")
    SHIPPING_INFO_LABEL: Tuple[By, str] = (By.CSS_SELECTOR, ".summary_info_label:nth-of-type(2)")
    SHIPPING_INFO_VALUE: Tuple[By, str] = (By.CSS_SELECTOR, ".summary_value_label:nth-of-type(2)")
    SUBTOTAL_LABEL: Tuple[By, str] = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL: Tuple[By, str] = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL: Tuple[By, str] = (By.CLASS_NAME, "summary_total_label")

    # Buttons
    CANCEL_BUTTON: Tuple[By, str] = (By.ID, "cancel")
    FINISH_BUTTON: Tuple[By, str] = (By.ID, "finish")

    def __init__(self, driver: WebDriver):
        """Initialize Checkout Step Two Page"""
        super().__init__(driver)
        self.logger.info("CheckoutStepTwoPage initialized")

    # ==================== Page Actions ====================

    def click_finish(self):
        """Click Finish button to complete order"""
        self.click(self.FINISH_BUTTON)
        self.logger.info("Clicked Finish to complete order")
        return self

    def click_cancel(self):
        """Click Cancel button"""
        self.click(self.CANCEL_BUTTON)
        return self

    # ==================== Page Getters ====================

    def get_item_count(self) -> int:
        """Get number of items in order"""
        items = self.find_elements(self.CART_ITEMS)
        return len(items)

    def get_all_item_names(self) -> List[str]:
        """Get list of all item names"""
        elements = self.find_elements(self.ITEM_NAMES)
        return [element.text for element in elements]

    def get_subtotal(self) -> float:
        """Get order subtotal"""
        text = self.get_text(self.SUBTOTAL_LABEL)
        # Format: "Item total: $XX.XX"
        price = text.split("$")[1]
        return float(price)

    def get_tax(self) -> float:
        """Get order tax"""
        text = self.get_text(self.TAX_LABEL)
        # Format: "Tax: $X.XX"
        price = text.split("$")[1]
        return float(price)

    def get_total(self) -> float:
        """Get order total"""
        text = self.get_text(self.TOTAL_LABEL)
        # Format: "Total: $XX.XX"
        price = text.split("$")[1]
        return float(price)

    def get_order_summary(self) -> Dict[str, any]:
        """Get complete order summary"""
        return {
            "item_count": self.get_item_count(),
            "items": self.get_all_item_names(),
            "subtotal": self.get_subtotal(),
            "tax": self.get_tax(),
            "total": self.get_total()
        }

    # ==================== Page Verifications ====================

    def is_checkout_step_two_displayed(self) -> bool:
        """Check if checkout step two page is displayed"""
        return self.is_element_visible(self.FINISH_BUTTON)

    def verify_total_calculation(self) -> bool:
        """Verify total = subtotal + tax"""
        subtotal = self.get_subtotal()
        tax = self.get_tax()
        total = self.get_total()
        expected_total = round(subtotal + tax, 2)
        return total == expected_total


class CheckoutCompletePage(BasePage):
    """
    Page Object for Checkout Complete Page
    URL: https://www.saucedemo.com/checkout-complete.html
    """

    # ==================== Locators ====================

    TITLE: Tuple[By, str] = (By.CLASS_NAME, "title")
    COMPLETE_HEADER: Tuple[By, str] = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT: Tuple[By, str] = (By.CLASS_NAME, "complete-text")
    PONY_EXPRESS_IMAGE: Tuple[By, str] = (By.CLASS_NAME, "pony_express")
    BACK_HOME_BUTTON: Tuple[By, str] = (By.ID, "back-to-products")

    def __init__(self, driver: WebDriver):
        """Initialize Checkout Complete Page"""
        super().__init__(driver)
        self.logger.info("CheckoutCompletePage initialized")

    # ==================== Page Actions ====================

    def click_back_home(self):
        """Click Back Home button"""
        self.click(self.BACK_HOME_BUTTON)
        self.logger.info("Clicked Back Home")
        return self

    # ==================== Page Getters ====================

    def get_complete_header(self) -> str:
        """Get completion header text"""
        return self.get_text(self.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        """Get completion message text"""
        return self.get_text(self.COMPLETE_TEXT)

    # ==================== Page Verifications ====================

    def is_order_complete(self) -> bool:
        """Check if order completion page is displayed"""
        return self.is_element_visible(self.COMPLETE_HEADER)

    def verify_order_success(self) -> bool:
        """Verify order was completed successfully"""
        header = self.get_complete_header()
        return "Thank you for your order" in header

    def verify_complete_message(self, expected_message: str) -> bool:
        """Verify completion message contains expected text"""
        actual_message = self.get_complete_text()
        return expected_message in actual_message


# Convenience alias
CheckoutPage = CheckoutStepOnePage
