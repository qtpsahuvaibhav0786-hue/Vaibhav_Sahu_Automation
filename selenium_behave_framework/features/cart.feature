@cart
Feature: Shopping Cart Functionality
  As a user with items in my cart
  I want to manage my cart contents
  So that I can proceed to checkout with my desired items

  Background:
    Given I am logged in as a standard user

  @smoke @positive
  Scenario: View empty cart
    When I navigate to the cart page
    Then the cart should be empty
    And I should see the "Continue Shopping" button
    And I should see the "Checkout" button

  @positive
  Scenario: View cart with single item
    Given I have added "Sauce Labs Backpack" to the cart
    When I navigate to the cart page
    Then I should see 1 item in the cart
    And I should see "Sauce Labs Backpack" in the cart
    And the item price should be displayed

  @positive
  Scenario: View cart with multiple items
    Given I have added the following items to the cart:
      | product                  |
      | Sauce Labs Backpack      |
      | Sauce Labs Bike Light    |
      | Sauce Labs Bolt T-Shirt  |
    When I navigate to the cart page
    Then I should see 3 items in the cart

  @positive
  Scenario: Remove item from cart
    Given I have added "Sauce Labs Backpack" to the cart
    And I have added "Sauce Labs Bike Light" to the cart
    When I navigate to the cart page
    And I remove "Sauce Labs Backpack" from the cart
    Then I should see 1 item in the cart
    And I should not see "Sauce Labs Backpack" in the cart
    And I should see "Sauce Labs Bike Light" in the cart

  @positive
  Scenario: Remove all items from cart
    Given I have added "Sauce Labs Backpack" to the cart
    And I have added "Sauce Labs Bike Light" to the cart
    When I navigate to the cart page
    And I remove all items from the cart
    Then the cart should be empty

  @navigation
  Scenario: Continue shopping from cart
    Given I have added "Sauce Labs Backpack" to the cart
    When I navigate to the cart page
    And I click "Continue Shopping"
    Then I should be on the inventory page
    And the cart badge should show "1"

  @navigation @checkout
  Scenario: Proceed to checkout from cart
    Given I have added "Sauce Labs Backpack" to the cart
    When I navigate to the cart page
    And I click "Checkout"
    Then I should be on the checkout information page

  @edge-case
  Scenario: Cart persists after page refresh
    Given I have added "Sauce Labs Backpack" to the cart
    When I refresh the page
    Then the cart badge should show "1"
    When I navigate to the cart page
    Then I should see "Sauce Labs Backpack" in the cart

  @edge-case
  Scenario: Cart persists after logout and login
    Given I have added "Sauce Labs Backpack" to the cart
    When I logout
    And I login as a standard user
    Then the cart badge should show "1"
