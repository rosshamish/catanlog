Feature: logging of the ending of a turn

  Scenario: player ends their turn
    Given it is "red"s turn
    When they end their turn
    Then it should look like "red ends turn after \d+s"
