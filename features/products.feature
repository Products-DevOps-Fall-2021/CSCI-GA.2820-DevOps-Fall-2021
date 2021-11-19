Feature: The product management service back-end
    As a Product management Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
    | name       | description  |  price| is_active | like |
    | grape      | fruit        | 2.9   |   True    |   1  |
    | bread      | food         | 3     |   True    |   0  | 
    | lamp       | electric     | 10    |   False   |   1  | 
    | apple      | fruit        | 1.8   |   True    |   1  | 
    | banana     | fruit        | 0.69  |   True    |   1  | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product REST Service" in the title
    And I should not see "404 Not Found"


 Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "peach"
    And I set the "Description" to "fruit"
    And I set the "Price" to "5"
    And I set the "is_active" to "True"
    And I set the "like" to "1"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "description" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "peach" in the "Name" field
    And I should see "fruit" in the "Description" field
    And I should see "5" in the "Price" field
    And I should see "True" in the "is_active" field
    And I should see "1" in the "like" field

Scenario: Read a Product
    When I visit the "Home Page" 
    And I set the "Name" to "grape"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Category" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "grape" in the "Name" field
    And I should see "fruit" in the "Description" field
    And I should see "2.9" in the "Price" field

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "grape"
    And I press the "Search" button
    Then I should see "grape" in the "Name" field
    And I should see "fruit" in the "desciption" field
    When I change "Name" to "pear"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see "pear" in the "Name" field


Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "grape" in the results
    And I should see "bead" in the results
    And I should see "lamp" in the results
    And I should see "apple" in the results
    And I should see "banana" in the results

Scenario: Search all products named grape
    When I visit the "Home Page"
    And I set the "Name" to "grape"
    And I press the "Search" button
    Then I should see "grape" in the results
    And I should not see "bread" in the results
    And I should not see "lamp" in the results
    And I should not see "apple" in the results
    And I should not see "banana" in the results

Scenario: Search all products price is 3
    When I visit the "Home Page"
    And I set the "Price" to "3"
    And I press the "Search" button
    Then I should see "bread" in the results
    And I should not see "grape" in the results
    And I should not see "lamp" in the results
    And I should not see "apple" in the results
    And I should not see "banana" in the results

Scenario: Search all products in description fruit
    When I visit the "Home Page"
    And I set the "Category" to "fruit"
    And I press the "Search" button
    Then I should see "grape" in the results
    And I should see "apple" in the results
    And I should see "banana" in the results
    And I should not see "bread" in the results
    And I should not see "lamp" in the results

Scenario: Search all products are active
    When I visit the "Home Page"
    And I set the "Owner" to "sun"
    And I press the "Search" button
    Then I should see "grape" in the results
    And I should see "bread" in the results
    And I should see "apple" in the results
    And I should see "banana" in the results
    And I should not see "lamp" in the results

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Name" to "apple"
    And I press the "Search" button
    Then I should see "apple" in the "Name" field
    And I should see "fruit" in the "description" field
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Delete" button
    Then I should see the message "Product has been Deleted!"
    




Scenario: Purchase a Product
    When I visit the "Home Page"
    And I set the "Name" to "grape"
    And I press the "Search" button
    Then I should see "grape" in the "Name" field
    And I should see "fruit" in the "description" field
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field to "Purchase_ID"
    And I set the "Amount" to "5"
    And I press the "Purchase" button
    Then I should see the message "Products has been Purchased successfully!"
