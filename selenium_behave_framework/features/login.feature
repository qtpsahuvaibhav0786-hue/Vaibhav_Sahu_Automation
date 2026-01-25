@login
Feature: Login Functionality
  As a user of Sauce Demo application
  I want to be able to login with valid credentials
  So that I can access the product inventory

  Background:
    Given I am on the login page

  @smoke @positive
  Scenario: Successful login with valid credentials
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should be redirected to the inventory page
    And I should see the products list

  @smoke @positive
  Scenario: Successful login as standard user
    When I login as a standard user
    Then I should be redirected to the inventory page

  @negative
  Scenario: Login with invalid username
    When I enter username "invalid_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should see an error message
    And the error message should contain "Username and password do not match"

  @negative
  Scenario: Login with invalid password
    When I enter username "standard_user"
    And I enter password "wrong_password"
    And I click the login button
    Then I should see an error message
    And the error message should contain "Username and password do not match"

  @negative
  Scenario: Login with locked out user
    When I enter username "locked_out_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should see an error message
    And the error message should contain "Sorry, this user has been locked out"

  @negative
  Scenario: Login with empty username
    When I enter username ""
    And I enter password "secret_sauce"
    And I click the login button
    Then I should see an error message
    And the error message should contain "Username is required"

  @negative
  Scenario: Login with empty password
    When I enter username "standard_user"
    And I enter password ""
    And I click the login button
    Then I should see an error message
    And the error message should contain "Password is required"

  @negative
  Scenario: Login with empty credentials
    When I click the login button
    Then I should see an error message
    And the error message should contain "Username is required"

  @data-driven
  Scenario Outline: Login with different user types
    When I enter username "<username>"
    And I enter password "<password>"
    And I click the login button
    Then I should see "<expected_result>"

    Examples:
      | username                | password     | expected_result   |
      | standard_user           | secret_sauce | inventory page    |
      | problem_user            | secret_sauce | inventory page    |
      | performance_glitch_user | secret_sauce | inventory page    |
      | locked_out_user         | secret_sauce | error message     |
      | invalid_user            | secret_sauce | error message     |
