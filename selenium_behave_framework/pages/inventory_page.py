"""
Inventory Page Object for Sauce Demo application
Represents the products listing page after login
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Tuple, List, Dict

from .base_page import BasePage


class InventoryPage(BasePage):
    """
    Page Object for Inventory/Products Page
    URL: https://www.saucedemo.com/inventory.html
    """

    # ==================== Locators ====================

    # Header elements
    APP_LOGO: Tuple[By, str] = (By.CLASS_NAME, "app_logo")
    MENU_BUTTON: Tuple[By, str] = (By.ID, "react-burger-menu-btn")
    SHOPPING_CART_LINK: Tuple[By, str] = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE: Tuple[By, str] = (By.CLASS_NAME, "shopping_cart_badge")

    # Menu items
    MENU_CLOSE_BUTTON: Tuple[By, str] = (By.ID, "react-burger-cross-btn")
    MENU_ALL_ITEMS: Tuple[By, str] = (By.ID, "inventory_sidebar_link")
    MENU_ABOUT: Tuple[By, str] = (By.ID, "about_sidebar_link")
    MENU_LOGOUT: Tuple[By, str] = (By.ID, "logout_sidebar_link")
    MENU_RESET: Tuple[By, str] = (By.ID, "reset_sidebar_link")

    # Product listing
    PRODUCT_CONTAINER: Tuple[By, str] = (By.CLASS_NAME, "inventory_container")
    PRODUCT_LIST: Tuple[By, str] = (By.CLASS_NAME, "inventory_list")
    PRODUCT_ITEMS: Tuple[By, str] = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES: Tuple[By, str] = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_DESCRIPTIONS: Tuple[By, str] = (By.CLASS_NAME, "inventory_item_desc")
    PRODUCT_PRICES: Tuple[By, str] = (By.CLASS_NAME, "inventory_item_price")
    PRODUCT_IMAGES: Tuple[By, str] = (By.CLASS_NAME, "inventory_item_img")

    # Sort dropdown
    SORT_DROPDOWN: Tuple[By, str] = (By.CLASS_NAME, "product_sort_container")

    # Add to cart buttons (dynamic)
    ADD_TO_CART_BUTTONS: Tuple[By, str] = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTONS: Tuple[By, str] = (By.CSS_SELECTOR, "button[id^='remove']")

    # Specific product add to cart buttons
    ADD_BACKPACK: Tuple[By, str] = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_BIKE_LIGHT: Tuple[By, str] = (By.ID, "add-to-cart-sauce-labs-bike-light")
    ADD_BOLT_TSHIRT: Tuple[By, str] = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    ADD_FLEECE_JACKET: Tuple[By, str] = (By.ID, "add-to-cart-sauce-labs-fleece-jacket")
    ADD_ONESIE: Tuple[By, str] = (By.ID, "add-to-cart-sauce-labs-onesie")
    ADD_RED_TSHIRT: Tuple[By, str] = (By.ID, "add-to-cart-test.allthethings()-t-shirt-(red)")

    # Footer
    FOOTER_TEXT: Tuple[By, str] = (By.CLASS_NAME, "footer_copy")
    TWITTER_LINK: Tuple[By, str] = (By.CSS_SELECTOR, "a[data-test='social-twitter']")
    FACEBOOK_LINK: Tuple[By, str] = (By.CSS_SELECTOR, "a[data-test='social-facebook']")
    LINKEDIN_LINK: Tuple[By, str] = (By.CSS_SELECTOR, "a[data-test='social-linkedin']")

    def __init__(self, driver: WebDriver):
        """Initialize Inventory Page"""
        super().__init__(driver)
        self.logger.info("InventoryPage initialized")

    # ==================== Page Actions ====================

    def open_menu(self):
        """Open hamburger menu"""
        self.click(self.MENU_BUTTON)
        self.explicit_wait(0.5)  # Wait for menu animation
        return self

    def close_menu(self):
        """Close hamburger menu"""
        self.click(self.MENU_CLOSE_BUTTON)
        return self

    def logout(self):
        """Logout from application"""
        self.open_menu()
        self.click(self.MENU_LOGOUT)
        self.logger.info("Logged out")
        return self

    def reset_app_state(self):
        """Reset application state"""
        self.open_menu()
        self.click(self.MENU_RESET)
        self.close_menu()
        return self

    def go_to_cart(self):
        """Navigate to shopping cart"""
        self.click(self.SHOPPING_CART_LINK)
        return self

    def add_product_to_cart(self, product_name: str):
        """
        Add a product to cart by name

        Args:
            product_name: Name of the product to add
        """
        product_id = product_name.lower().replace(" ", "-")
        add_button = (By.ID, f"add-to-cart-{product_id}")
        self.click(add_button)
        self.logger.info(f"Added {product_name} to cart")
        return self

    def remove_product_from_cart(self, product_name: str):
        """
        Remove a product from cart by name

        Args:
            product_name: Name of the product to remove
        """
        product_id = product_name.lower().replace(" ", "-")
        remove_button = (By.ID, f"remove-{product_id}")
        self.click(remove_button)
        self.logger.info(f"Removed {product_name} from cart")
        return self

    def add_backpack_to_cart(self):
        """Add Sauce Labs Backpack to cart"""
        self.click(self.ADD_BACKPACK)
        return self

    def add_bike_light_to_cart(self):
        """Add Sauce Labs Bike Light to cart"""
        self.click(self.ADD_BIKE_LIGHT)
        return self

    def add_bolt_tshirt_to_cart(self):
        """Add Sauce Labs Bolt T-Shirt to cart"""
        self.click(self.ADD_BOLT_TSHIRT)
        return self

    def add_fleece_jacket_to_cart(self):
        """Add Sauce Labs Fleece Jacket to cart"""
        self.click(self.ADD_FLEECE_JACKET)
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

    def sort_products(self, sort_option: str):
        """
        Sort products by given option

        Args:
            sort_option: Sort option value (az, za, lohi, hilo)
        """
        self.select_by_value(self.SORT_DROPDOWN, sort_option)
        self.logger.info(f"Sorted products by: {sort_option}")
        return self

    def sort_by_name_az(self):
        """Sort products by name A to Z"""
        return self.sort_products("az")

    def sort_by_name_za(self):
        """Sort products by name Z to A"""
        return self.sort_products("za")

    def sort_by_price_low_high(self):
        """Sort products by price low to high"""
        return self.sort_products("lohi")

    def sort_by_price_high_low(self):
        """Sort products by price high to low"""
        return self.sort_products("hilo")

    # ==================== Page Getters ====================

    def get_product_count(self) -> int:
        """Get total number of products displayed"""
        products = self.find_elements(self.PRODUCT_ITEMS)
        return len(products)

    def get_cart_count(self) -> int:
        """Get number of items in cart"""
        if self.is_element_visible(self.SHOPPING_CART_BADGE, timeout=2):
            count_text = self.get_text(self.SHOPPING_CART_BADGE)
            return int(count_text) if count_text else 0
        return 0

    def get_all_product_names(self) -> List[str]:
        """Get list of all product names"""
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [element.text for element in elements]

    def get_all_product_prices(self) -> List[float]:
        """Get list of all product prices"""
        elements = self.find_elements(self.PRODUCT_PRICES)
        prices = []
        for element in elements:
            price_text = element.text.replace("$", "")
            prices.append(float(price_text))
        return prices

    def get_product_info(self, product_name: str) -> Dict[str, str]:
        """
        Get product information by name

        Args:
            product_name: Name of the product

        Returns:
            Dictionary with product details
        """
        product_item = (By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']")
        item = self.find_element(product_item)

        name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
        desc = item.find_element(By.CLASS_NAME, "inventory_item_desc").text
        price = item.find_element(By.CLASS_NAME, "inventory_item_price").text

        return {
            "name": name,
            "description": desc,
            "price": price
        }

    # ==================== Page Verifications ====================

    def is_inventory_page_displayed(self) -> bool:
        """Check if inventory page is displayed"""
        return self.is_element_visible(self.PRODUCT_CONTAINER)

    def is_product_displayed(self, product_name: str) -> bool:
        """Check if specific product is displayed"""
        product_locator = (By.XPATH, f"//div[text()='{product_name}']")
        return self.is_element_visible(product_locator, timeout=5)

    def is_product_added_to_cart(self, product_name: str) -> bool:
        """Check if product has Remove button (meaning it's in cart)"""
        product_id = product_name.lower().replace(" ", "-")
        remove_button = (By.ID, f"remove-{product_id}")
        return self.is_element_visible(remove_button, timeout=2)

    def verify_products_sorted_az(self) -> bool:
        """Verify products are sorted A to Z"""
        names = self.get_all_product_names()
        return names == sorted(names)

    def verify_products_sorted_za(self) -> bool:
        """Verify products are sorted Z to A"""
        names = self.get_all_product_names()
        return names == sorted(names, reverse=True)

    def verify_products_sorted_price_low_high(self) -> bool:
        """Verify products are sorted by price low to high"""
        prices = self.get_all_product_prices()
        return prices == sorted(prices)

    def verify_products_sorted_price_high_low(self) -> bool:
        """Verify products are sorted by price high to low"""
        prices = self.get_all_product_prices()
        return prices == sorted(prices, reverse=True)
