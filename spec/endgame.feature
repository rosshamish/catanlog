Feature: logging of the end of the game

  Scenario: a player wins the game
    Given it is "red"s turn
    When they win the game
    Then it should look exactly like "red wins"
