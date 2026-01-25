"""
Step definitions for login feature
"""

from behave import given, when, then
from selenium_behave_framework.pages.login_page import LoginPage
from selenium_behave_framework.pages.inventory_page import InventoryPage


@given('I am on the login page')
def step_on_login_page(context):
    """Navigate to login page"""
    context.login_page = LoginPage(context.driver)
    context.login_page.open()
    assert context.login_page.is_login_page_displayed(), "Login page is not displayed"


@when('I enter username "{username}"')
def step_enter_username(context, username):
    """Enter username in login form"""
    context.login_page.enter_username(username)


@when('I enter password "{password}"')
def step_enter_password(context, password):
    """Enter password in login form"""
    context.login_page.enter_password(password)


@when('I click the login button')
def step_click_login(context):
    """Click login button"""
    context.login_page.click_login()


@when('I login as a standard user')
def step_login_standard_user(context):
    """Login as standard user"""
    context.login_page.login_as_standard_user()


@when('I login with username "{username}" and password "{password}"')
def step_login_with_credentials(context, username, password):
    """Login with specified credentials"""
    context.login_page.login(username, password)


@then('I should be redirected to the inventory page')
def step_verify_inventory_page(context):
    """Verify user is on inventory page"""
    context.inventory_page = InventoryPage(context.driver)
    assert context.inventory_page.is_inventory_page_displayed(), "Inventory page is not displayed"


@then('I should see the products list')
def step_verify_products_list(context):
    """Verify products list is visible"""
    if not hasattr(context, 'inventory_page'):
        context.inventory_page = InventoryPage(context.driver)
    assert context.inventory_page.get_product_count() > 0, "No products displayed"


@then('I should see an error message')
def step_verify_error_displayed(context):
    """Verify error message is displayed"""
    assert context.login_page.is_error_displayed(), "Error message is not displayed"


@then('the error message should contain "{expected_text}"')
def step_verify_error_text(context, expected_text):
    """Verify error message contains expected text"""
    assert context.login_page.verify_error_message(expected_text), \
        f"Error message does not contain '{expected_text}'"


@then('I should see "{expected_result}"')
def step_verify_expected_result(context, expected_result):
    """Verify expected result based on scenario"""
    if expected_result == "inventory page":
        context.inventory_page = InventoryPage(context.driver)
        assert context.inventory_page.is_inventory_page_displayed(), "Inventory page is not displayed"
    elif expected_result == "error message":
        assert context.login_page.is_error_displayed(), "Error message is not displayed"
    else:
        raise ValueError(f"Unknown expected result: {expected_result}")


@given('I am logged in as a standard user')
def step_logged_in_standard_user(context):
    """Login as standard user"""
    context.login_page = LoginPage(context.driver)
    context.login_page.open()
    context.login_page.login_as_standard_user()
    context.inventory_page = InventoryPage(context.driver)
    assert context.inventory_page.is_inventory_page_displayed(), "Failed to login"


@when('I logout')
def step_logout(context):
    """Logout from application"""
    if not hasattr(context, 'inventory_page'):
        context.inventory_page = InventoryPage(context.driver)
    context.inventory_page.logout()


@then('I should be redirected to the login page')
def step_verify_login_page_redirect(context):
    """Verify user is redirected to login page"""
    context.login_page = LoginPage(context.driver)
    assert context.login_page.is_login_page_displayed(), "Not redirected to login page"


@when('I login as a standard user')
def step_when_login_standard_user(context):
    """Login as standard user (when step)"""
    context.login_page = LoginPage(context.driver)
    context.login_page.open()
    context.login_page.login_as_standard_user()
