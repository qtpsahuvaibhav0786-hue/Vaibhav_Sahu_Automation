@checkout
Feature: Checkout Process
  As a user with items in my cart
  I want to complete the checkout process
  So that I can purchase my selected items

  Background:
    Given I am logged in as a standard user
    And I have added "Sauce Labs Backpack" to the cart
    And I navigate to the cart page
    And I proceed to checkout

  @smoke @positive
  Scenario: Complete checkout with valid information
    When I enter first name "John"
    And I enter last name "Doe"
    And I enter postal code "12345"
    And I click continue
    Then I should be on the checkout overview page
    When I click finish
    Then I should see the order confirmation
    And the confirmation message should contain "Thank you for your order"

  @positive
  Scenario: View order summary before completing
    When I fill checkout information with:
      | first_name | last_name | postal_code |
      | John       | Doe       | 12345       |
    And I click continue
    Then I should be on the checkout overview page
    And I should see "Sauce Labs Backpack" in the order summary
    And I should see the payment information
    And I should see the shipping information
    And I should see the subtotal
    And I should see the tax
    And I should see the total

  @positive
  Scenario: Verify total calculation
    When I fill checkout information with:
      | first_name | last_name | postal_code |
      | John       | Doe       | 12345       |
    And I click continue
    Then the total should equal subtotal plus tax

  @negative
  Scenario: Checkout with empty first name
    When I enter first name ""
    And I enter last name "Doe"
    And I enter postal code "12345"
    And I click continue
    Then I should see a checkout error
    And the error message should contain "First Name is required"

  @negative
  Scenario: Checkout with empty last name
    When I enter first name "John"
    And I enter last name ""
    And I enter postal code "12345"
    And I click continue
    Then I should see a checkout error
    And the error message should contain "Last Name is required"

  @negative
  Scenario: Checkout with empty postal code
    When I enter first name "John"
    And I enter last name "Doe"
    And I enter postal code ""
    And I click continue
    Then I should see a checkout error
    And the error message should contain "Postal Code is required"

  @negative
  Scenario: Checkout with all empty fields
    When I click continue
    Then I should see a checkout error
    And the error message should contain "First Name is required"

  @navigation
  Scenario: Cancel from checkout step one
    When I click cancel on checkout step one
    Then I should be on the cart page

  @navigation
  Scenario: Cancel from checkout step two
    When I fill checkout information with:
      | first_name | last_name | postal_code |
      | John       | Doe       | 12345       |
    And I click continue
    When I click cancel on checkout step two
    Then I should be on the inventory page

  @positive
  Scenario: Return to products after order completion
    When I complete the checkout process
    Then I should see the order confirmation
    When I click "Back Home"
    Then I should be on the inventory page
