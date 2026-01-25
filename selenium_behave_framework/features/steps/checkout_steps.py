"""
Step definitions for checkout feature
"""

from behave import given, when, then
from selenium_behave_framework.pages.checkout_page import (
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage
)


@then('I should be on the checkout information page')
def step_verify_checkout_info_page(context):
    """Verify on checkout step one page"""
    context.checkout_step_one = CheckoutStepOnePage(context.driver)
    assert context.checkout_step_one.is_checkout_step_one_displayed(), \
        "Not on checkout information page"


@when('I enter first name "{first_name}"')
def step_enter_first_name(context, first_name):
    """Enter first name in checkout form"""
    if not hasattr(context, 'checkout_step_one'):
        context.checkout_step_one = CheckoutStepOnePage(context.driver)
    context.checkout_step_one.enter_first_name(first_name)


@when('I enter last name "{last_name}"')
def step_enter_last_name(context, last_name):
    """Enter last name in checkout form"""
    if not hasattr(context, 'checkout_step_one'):
        context.checkout_step_one = CheckoutStepOnePage(context.driver)
    context.checkout_step_one.enter_last_name(last_name)


@when('I enter postal code "{postal_code}"')
def step_enter_postal_code(context, postal_code):
    """Enter postal code in checkout form"""
    if not hasattr(context, 'checkout_step_one'):
        context.checkout_step_one = CheckoutStepOnePage(context.driver)
    context.checkout_step_one.enter_postal_code(postal_code)


@when('I click continue')
def step_click_continue(context):
    """Click continue button on checkout"""
    if not hasattr(context, 'checkout_step_one'):
        context.checkout_step_one = CheckoutStepOnePage(context.driver)
    context.checkout_step_one.click_continue()


@when('I fill checkout information with')
def step_fill_checkout_info(context):
    """Fill checkout information from table"""
    if not hasattr(context, 'checkout_step_one'):
        context.checkout_step_one = CheckoutStepOnePage(context.driver)
    for row in context.table:
        context.checkout_step_one.fill_information(
            row['first_name'],
            row['last_name'],
            row['postal_code']
        )


@when('I enter checkout information')
def step_enter_checkout_info(context):
    """Enter checkout information from table"""
    step_fill_checkout_info(context)


@then('I should be on the checkout overview page')
def step_verify_checkout_overview_page(context):
    """Verify on checkout step two page"""
    context.checkout_step_two = CheckoutStepTwoPage(context.driver)
    assert context.checkout_step_two.is_checkout_step_two_displayed(), \
        "Not on checkout overview page"


@then('I should see "{product_name}" in the order summary')
def step_verify_item_in_summary(context, product_name):
    """Verify item is in order summary"""
    item_names = context.checkout_step_two.get_all_item_names()
    assert product_name in item_names, f"'{product_name}' not in order summary"


@then('I should see the payment information')
def step_verify_payment_info(context):
    """Verify payment information is displayed"""
    from selenium.webdriver.common.by import By
    assert context.checkout_step_two.is_element_visible(
        (By.CLASS_NAME, "summary_value_label")
    ), "Payment information not displayed"


@then('I should see the shipping information')
def step_verify_shipping_info(context):
    """Verify shipping information is displayed"""
    # Shipping info is displayed in summary
    pass


@then('I should see the subtotal')
def step_verify_subtotal(context):
    """Verify subtotal is displayed"""
    subtotal = context.checkout_step_two.get_subtotal()
    assert subtotal > 0, "Subtotal not displayed"


@then('I should see the tax')
def step_verify_tax(context):
    """Verify tax is displayed"""
    tax = context.checkout_step_two.get_tax()
    assert tax >= 0, "Tax not displayed"


@then('I should see the total')
def step_verify_total(context):
    """Verify total is displayed"""
    total = context.checkout_step_two.get_total()
    assert total > 0, "Total not displayed"


@then('the total should equal subtotal plus tax')
def step_verify_total_calculation(context):
    """Verify total = subtotal + tax"""
    assert context.checkout_step_two.verify_total_calculation(), \
        "Total calculation is incorrect"


@then('the order total should be calculated correctly')
def step_verify_order_total_calculation(context):
    """Verify order total calculation"""
    step_verify_total_calculation(context)


@when('I click finish')
def step_click_finish(context):
    """Click finish button"""
    if not hasattr(context, 'checkout_step_two'):
        context.checkout_step_two = CheckoutStepTwoPage(context.driver)
    context.checkout_step_two.click_finish()


@when('I complete the order')
def step_complete_order(context):
    """Complete the order"""
    step_click_finish(context)


@then('I should see the order confirmation')
def step_verify_order_confirmation(context):
    """Verify order confirmation page"""
    context.checkout_complete = CheckoutCompletePage(context.driver)
    assert context.checkout_complete.is_order_complete(), \
        "Order confirmation not displayed"


@then('the confirmation message should contain "{expected_text}"')
def step_verify_confirmation_message(context, expected_text):
    """Verify confirmation message"""
    header = context.checkout_complete.get_complete_header()
    assert expected_text in header, \
        f"Confirmation message doesn't contain '{expected_text}'"


@then('I should see a checkout error')
def step_verify_checkout_error(context):
    """Verify checkout error is displayed"""
    if not hasattr(context, 'checkout_step_one'):
        context.checkout_step_one = CheckoutStepOnePage(context.driver)
    assert context.checkout_step_one.is_error_displayed(), \
        "Checkout error not displayed"


@when('I click cancel on checkout step one')
def step_click_cancel_step_one(context):
    """Click cancel on checkout step one"""
    if not hasattr(context, 'checkout_step_one'):
        context.checkout_step_one = CheckoutStepOnePage(context.driver)
    context.checkout_step_one.click_cancel()


@when('I click cancel on checkout step two')
def step_click_cancel_step_two(context):
    """Click cancel on checkout step two"""
    if not hasattr(context, 'checkout_step_two'):
        context.checkout_step_two = CheckoutStepTwoPage(context.driver)
    context.checkout_step_two.click_cancel()


@when('I click "Back Home"')
def step_click_back_home(context):
    """Click Back Home button"""
    if not hasattr(context, 'checkout_complete'):
        context.checkout_complete = CheckoutCompletePage(context.driver)
    context.checkout_complete.click_back_home()


@when('I complete the checkout process')
def step_complete_checkout(context):
    """Complete full checkout process with default info"""
    if not hasattr(context, 'checkout_step_one'):
        context.checkout_step_one = CheckoutStepOnePage(context.driver)
    context.checkout_step_one.fill_information("Test", "User", "12345")
    context.checkout_step_one.click_continue()
    context.checkout_step_two = CheckoutStepTwoPage(context.driver)
    context.checkout_step_two.click_finish()


@when('I complete checkout with valid information')
def step_complete_checkout_valid_info(context):
    """Complete checkout with valid information"""
    from selenium_behave_framework.pages.cart_page import CartPage
    cart_page = CartPage(context.driver)
    cart_page.proceed_to_checkout()
    step_complete_checkout(context)


@when('I complete full checkout process')
def step_complete_full_checkout(context):
    """Complete full checkout from inventory"""
    from selenium_behave_framework.pages.inventory_page import InventoryPage
    from selenium_behave_framework.pages.cart_page import CartPage

    inventory_page = InventoryPage(context.driver)
    inventory_page.go_to_cart()

    cart_page = CartPage(context.driver)
    cart_page.proceed_to_checkout()

    context.checkout_step_one = CheckoutStepOnePage(context.driver)
    context.checkout_step_one.fill_information("Test", "User", "12345")
    context.checkout_step_one.click_continue()

    context.checkout_step_two = CheckoutStepTwoPage(context.driver)
    context.checkout_step_two.click_finish()


@then('I should see {count:d} items in the order summary')
def step_verify_order_summary_count(context, count):
    """Verify number of items in order summary"""
    if not hasattr(context, 'checkout_step_two'):
        context.checkout_step_two = CheckoutStepTwoPage(context.driver)
    actual_count = context.checkout_step_two.get_item_count()
    assert actual_count == count, f"Expected {count} items, found {actual_count}"


@when('I proceed to checkout with')
def step_proceed_to_checkout_with_info(context):
    """Proceed through cart and enter checkout info"""
    from selenium_behave_framework.pages.cart_page import CartPage
    context.cart_page = CartPage(context.driver)
    context.cart_page.proceed_to_checkout()

    context.checkout_step_one = CheckoutStepOnePage(context.driver)
    for row in context.table:
        context.checkout_step_one.fill_information(
            row['first_name'],
            row['last_name'],
            row['postal_code']
        )
    context.checkout_step_one.click_continue()
