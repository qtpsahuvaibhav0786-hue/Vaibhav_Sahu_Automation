"""
Step definitions for cart feature
"""

from behave import given, when, then
from selenium_behave_framework.pages.cart_page import CartPage
from selenium_behave_framework.pages.inventory_page import InventoryPage


@when('I navigate to the cart page')
def step_navigate_to_cart(context):
    """Navigate to cart page"""
    if not hasattr(context, 'inventory_page'):
        context.inventory_page = InventoryPage(context.driver)
    context.inventory_page.go_to_cart()
    context.cart_page = CartPage(context.driver)


@given('I navigate to the cart page')
def step_given_navigate_to_cart(context):
    """Navigate to cart page (given)"""
    step_navigate_to_cart(context)


@then('I should be on the cart page')
def step_verify_cart_page(context):
    """Verify on cart page"""
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    assert context.cart_page.is_cart_page_displayed(), "Not on cart page"


@then('the cart should be empty')
def step_verify_cart_empty(context):
    """Verify cart is empty"""
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    assert context.cart_page.is_cart_empty(), "Cart is not empty"


@then('I should see the "Continue Shopping" button')
def step_verify_continue_shopping_button(context):
    """Verify Continue Shopping button is visible"""
    from selenium.webdriver.common.by import By
    assert context.cart_page.is_element_visible((By.ID, "continue-shopping")), \
        "Continue Shopping button not visible"


@then('I should see the "Checkout" button')
def step_verify_checkout_button(context):
    """Verify Checkout button is visible"""
    from selenium.webdriver.common.by import By
    assert context.cart_page.is_element_visible((By.ID, "checkout")), \
        "Checkout button not visible"


@then('I should see {count:d} item in the cart')
def step_verify_cart_item_count_singular(context, count):
    """Verify number of items in cart (singular)"""
    actual_count = context.cart_page.get_cart_items_count()
    assert actual_count == count, f"Expected {count} item, found {actual_count}"


@then('I should see {count:d} items in the cart')
def step_verify_cart_item_count_plural(context, count):
    """Verify number of items in cart (plural)"""
    actual_count = context.cart_page.get_cart_items_count()
    assert actual_count == count, f"Expected {count} items, found {actual_count}"


@then('I should see "{product_name}" in the cart')
def step_verify_item_in_cart(context, product_name):
    """Verify item is in cart"""
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    assert context.cart_page.is_item_in_cart(product_name), \
        f"'{product_name}' not found in cart"


@then('I should not see "{product_name}" in the cart')
def step_verify_item_not_in_cart(context, product_name):
    """Verify item is not in cart"""
    assert not context.cart_page.is_item_in_cart(product_name), \
        f"'{product_name}' should not be in cart"


@then('the item price should be displayed')
def step_verify_item_price_displayed(context):
    """Verify item prices are displayed"""
    prices = context.cart_page.get_all_item_prices()
    assert len(prices) > 0, "No item prices displayed"


@then('the item price should be "{price}"')
def step_verify_specific_item_price(context, price):
    """Verify specific item price"""
    prices = context.cart_page.get_all_item_prices()
    expected_price = float(price.replace("$", ""))
    assert expected_price in prices, f"Price {price} not found in cart"


@when('I remove "{product_name}" from the cart')
def step_remove_item_from_cart(context, product_name):
    """Remove item from cart"""
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    context.cart_page.remove_item(product_name)


@when('I remove all items from the cart')
def step_remove_all_items(context):
    """Remove all items from cart"""
    context.cart_page.remove_all_items()


@when('I click "Continue Shopping"')
def step_click_continue_shopping(context):
    """Click Continue Shopping button"""
    context.cart_page.continue_shopping()


@when('I click "Checkout"')
def step_click_checkout(context):
    """Click Checkout button"""
    context.cart_page.proceed_to_checkout()


@then('I should be on the inventory page')
def step_verify_inventory_page(context):
    """Verify on inventory page"""
    if not hasattr(context, 'inventory_page'):
        context.inventory_page = InventoryPage(context.driver)
    assert context.inventory_page.is_inventory_page_displayed(), "Not on inventory page"


@when('I refresh the page')
def step_refresh_page(context):
    """Refresh current page"""
    context.driver.refresh()


@when('I proceed to checkout')
def step_proceed_to_checkout(context):
    """Proceed to checkout from cart"""
    if not hasattr(context, 'cart_page'):
        context.cart_page = CartPage(context.driver)
    context.cart_page.proceed_to_checkout()


@given('I proceed to checkout')
def step_given_proceed_to_checkout(context):
    """Proceed to checkout from cart (given)"""
    step_proceed_to_checkout(context)
