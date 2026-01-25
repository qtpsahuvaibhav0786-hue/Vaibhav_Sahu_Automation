@e2e @smoke
Feature: End-to-End Shopping Flow
  As a customer
  I want to complete a full shopping experience
  From login to order completion

  @critical
  Scenario: Complete purchase flow with single item
    Given I am on the login page
    When I login with username "standard_user" and password "secret_sauce"
    Then I should be redirected to the inventory page

    When I add "Sauce Labs Backpack" to the cart
    Then the cart badge should show "1"

    When I click on the cart icon
    Then I should be on the cart page
    And I should see "Sauce Labs Backpack" in the cart

    When I click "Checkout"
    Then I should be on the checkout information page

    When I enter checkout information:
      | first_name | last_name | postal_code |
      | Test       | User      | 90210       |
    And I click continue
    Then I should be on the checkout overview page
    And the order total should be calculated correctly

    When I click finish
    Then I should see the order confirmation
    And the confirmation message should contain "Thank you for your order"

  @critical
  Scenario: Complete purchase flow with multiple items
    Given I am on the login page
    When I login with username "standard_user" and password "secret_sauce"
    Then I should be redirected to the inventory page

    When I add the following products to cart:
      | product                  |
      | Sauce Labs Backpack      |
      | Sauce Labs Bike Light    |
      | Sauce Labs Bolt T-Shirt  |
    Then the cart badge should show "3"

    When I click on the cart icon
    And I proceed to checkout with:
      | first_name | last_name | postal_code |
      | Test       | User      | 90210       |
    Then I should be on the checkout overview page
    And I should see 3 items in the order summary

    When I complete the order
    Then I should see the order confirmation

  @regression
  Scenario: Add and remove items before checkout
    Given I am logged in as a standard user
    And I am on the inventory page

    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    And I add "Sauce Labs Fleece Jacket" to the cart
    Then the cart badge should show "3"

    When I remove "Sauce Labs Bike Light" from the cart
    Then the cart badge should show "2"

    When I click on the cart icon
    Then I should see 2 items in the cart
    And I should not see "Sauce Labs Bike Light" in the cart

    When I complete checkout with valid information
    Then I should see the order confirmation

  @regression
  Scenario: Verify product details before purchase
    Given I am logged in as a standard user
    And I am on the inventory page

    When I click on product "Sauce Labs Backpack"
    Then I should see the product details page
    And the product price should be "$29.99"

    When I add the product to cart from details page
    And I navigate to cart
    Then the item price should be "$29.99"

  @performance
  Scenario: Complete purchase with performance glitch user
    Given I am on the login page
    When I login with username "performance_glitch_user" and password "secret_sauce"
    Then I should be redirected to the inventory page

    When I add "Sauce Labs Onesie" to the cart
    And I complete full checkout process
    Then I should see the order confirmation
