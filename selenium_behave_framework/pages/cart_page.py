"""
Cart Page Object for Sauce Demo application
Represents the shopping cart page
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Tuple, List, Dict

from .base_page import BasePage


class CartPage(BasePage):
    """
    Page Object for Shopping Cart Page
    URL: https://www.saucedemo.com/cart.html
    """

    # ==================== Locators ====================

    # Header
    TITLE: Tuple[By, str] = (By.CLASS_NAME, "title")

    # Cart items
    CART_LIST: Tuple[By, str] = (By.CLASS_NAME, "cart_list")
    CART_ITEMS: Tuple[By, str] = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAMES: Tuple[By, str] = (By.CLASS_NAME, "inventory_item_name")
    CART_ITEM_DESCRIPTIONS: Tuple[By, str] = (By.CLASS_NAME, "inventory_item_desc")
    CART_ITEM_PRICES: Tuple[By, str] = (By.CLASS_NAME, "inventory_item_price")
    CART_ITEM_QUANTITIES: Tuple[By, str] = (By.CLASS_NAME, "cart_quantity")
    REMOVE_BUTTONS: Tuple[By, str] = (By.CSS_SELECTOR, "button[id^='remove']")

    # Action buttons
    CONTINUE_SHOPPING_BUTTON: Tuple[By, str] = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON: Tuple[By, str] = (By.ID, "checkout")

    # Cart badge
    CART_BADGE: Tuple[By, str] = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver: WebDriver):
        """Initialize Cart Page"""
        super().__init__(driver)
        self.logger.info("CartPage initialized")

    # ==================== Page Actions ====================

    def continue_shopping(self):
        """Click Continue Shopping button"""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        self.logger.info("Clicked Continue Shopping")
        return self

    def proceed_to_checkout(self):
        """Click Checkout button"""
        self.click(self.CHECKOUT_BUTTON)
        self.logger.info("Clicked Checkout")
        return self

    def remove_item(self, product_name: str):
        """
        Remove item from cart by product name

        Args:
            product_name: Name of the product to remove
        """
        product_id = product_name.lower().replace(" ", "-")
        remove_button = (By.ID, f"remove-{product_id}")
        self.click(remove_button)
        self.logger.info(f"Removed {product_name} from cart")
        return self

    def remove_all_items(self):
        """Remove all items from cart"""
        remove_buttons = self.find_elements(self.REMOVE_BUTTONS, wait_for_presence=False)
        for button in remove_buttons:
            button.click()
        self.logger.info("Removed all items from cart")
        return self

    def click_product(self, product_name: str):
        """
        Click on a product to view details

        Args:
            product_name: Name of the product to click
        """
        product_link = (By.XPATH, f"//div[text()='{product_name}']")
        self.click(product_link)
        return self

    # ==================== Page Getters ====================

    def get_cart_items_count(self) -> int:
        """Get number of items in cart"""
        items = self.find_elements(self.CART_ITEMS, wait_for_presence=False)
        return len(items)

    def get_cart_badge_count(self) -> int:
        """Get cart badge count"""
        if self.is_element_visible(self.CART_BADGE, timeout=2):
            count_text = self.get_text(self.CART_BADGE)
            return int(count_text) if count_text else 0
        return 0

    def get_all_item_names(self) -> List[str]:
        """Get list of all item names in cart"""
        elements = self.find_elements(self.CART_ITEM_NAMES, wait_for_presence=False)
        return [element.text for element in elements]

    def get_all_item_prices(self) -> List[float]:
        """Get list of all item prices in cart"""
        elements = self.find_elements(self.CART_ITEM_PRICES, wait_for_presence=False)
        prices = []
        for element in elements:
            price_text = element.text.replace("$", "")
            prices.append(float(price_text))
        return prices

    def get_cart_total(self) -> float:
        """Calculate total price of all items in cart"""
        prices = self.get_all_item_prices()
        return sum(prices)

    def get_item_quantity(self, product_name: str) -> int:
        """
        Get quantity of specific item in cart

        Args:
            product_name: Name of the product

        Returns:
            Quantity of the item
        """
        item_row = (By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='cart_item']")
        item = self.find_element(item_row)
        quantity_element = item.find_element(By.CLASS_NAME, "cart_quantity")
        return int(quantity_element.text)

    def get_item_info(self, product_name: str) -> Dict[str, str]:
        """
        Get item information by name

        Args:
            product_name: Name of the product

        Returns:
            Dictionary with item details
        """
        item_row = (By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='cart_item']")
        item = self.find_element(item_row)

        name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
        desc = item.find_element(By.CLASS_NAME, "inventory_item_desc").text
        price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
        quantity = item.find_element(By.CLASS_NAME, "cart_quantity").text

        return {
            "name": name,
            "description": desc,
            "price": price,
            "quantity": quantity
        }

    # ==================== Page Verifications ====================

    def is_cart_page_displayed(self) -> bool:
        """Check if cart page is displayed"""
        return self.is_element_visible(self.CART_LIST)

    def is_cart_empty(self) -> bool:
        """Check if cart is empty"""
        return self.get_cart_items_count() == 0

    def is_item_in_cart(self, product_name: str) -> bool:
        """
        Check if specific item is in cart

        Args:
            product_name: Name of the product

        Returns:
            True if item is in cart
        """
        item_names = self.get_all_item_names()
        return product_name in item_names

    def verify_item_count(self, expected_count: int) -> bool:
        """
        Verify number of items in cart

        Args:
            expected_count: Expected number of items

        Returns:
            True if count matches
        """
        actual_count = self.get_cart_items_count()
        matches = actual_count == expected_count
        self.logger.info(f"Item count verification: expected={expected_count}, actual={actual_count}, matches={matches}")
        return matches

    def verify_item_price(self, product_name: str, expected_price: float) -> bool:
        """
        Verify price of specific item

        Args:
            product_name: Name of the product
            expected_price: Expected price

        Returns:
            True if price matches
        """
        item_info = self.get_item_info(product_name)
        actual_price = float(item_info["price"].replace("$", ""))
        return actual_price == expected_price
