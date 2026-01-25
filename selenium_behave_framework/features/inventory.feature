@inventory
Feature: Inventory Page Functionality
  As a logged-in user
  I want to browse and interact with products
  So that I can add items to my cart

  Background:
    Given I am logged in as a standard user
    And I am on the inventory page

  @smoke @positive
  Scenario: View all products
    Then I should see the products list
    And I should see 6 products displayed

  @positive
  Scenario: Add single product to cart
    When I add "Sauce Labs Backpack" to the cart
    Then the cart badge should show "1"
    And the product should show "Remove" button

  @positive
  Scenario: Add multiple products to cart
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    And I add "Sauce Labs Bolt T-Shirt" to the cart
    Then the cart badge should show "3"

  @positive
  Scenario: Remove product from cart
    Given I have added "Sauce Labs Backpack" to the cart
    When I remove "Sauce Labs Backpack" from the cart
    Then the cart badge should not be visible
    And the product should show "Add to cart" button

  @sorting
  Scenario: Sort products by name A to Z
    When I sort products by "Name (A to Z)"
    Then the products should be sorted alphabetically ascending

  @sorting
  Scenario: Sort products by name Z to A
    When I sort products by "Name (Z to A)"
    Then the products should be sorted alphabetically descending

  @sorting
  Scenario: Sort products by price low to high
    When I sort products by "Price (low to high)"
    Then the products should be sorted by price ascending

  @sorting
  Scenario: Sort products by price high to low
    When I sort products by "Price (high to low)"
    Then the products should be sorted by price descending

  @navigation
  Scenario: Navigate to product details
    When I click on product "Sauce Labs Backpack"
    Then I should see the product details page
    And the product name should be "Sauce Labs Backpack"

  @navigation
  Scenario: Navigate to cart from inventory
    When I click on the cart icon
    Then I should be on the cart page

  @menu
  Scenario: Logout from inventory page
    When I open the menu
    And I click on logout
    Then I should be redirected to the login page

  @menu
  Scenario: Reset application state
    Given I have added "Sauce Labs Backpack" to the cart
    And I have added "Sauce Labs Bike Light" to the cart
    When I open the menu
    And I reset the application state
    Then the cart badge should not be visible
