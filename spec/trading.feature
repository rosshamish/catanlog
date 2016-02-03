Feature: logging of trades between player<->port, and player<->player

  Scenario: basic trade between player and 3:1 port
    Given it is "red"s turn
    When they trade "wood" for "ore" with a "3:1" port
    Then it should look exactly like "red trades [3 wood] to port 3:1 for [1 ore]"

  Scenario: compound trade between player and 3:1 port
    Given it is "white"s turn
    When they trade "3" "wood" and "3 brick" for "ore" with a "3:1" port
    Then it should look exactly like "white trades [3 wood, 3 brick] to port 3:1 for [2 ore]"

  Scenario: basic trade between player and 4:1 port
    Given it is "blue"s turn
    When they trade "wood" for "ore" with a "4:1" port
    Then it should look exactly like "blue trades [4 wood] to port 4:1 for [1 ore]"

  Scenario: basic trade between player and wood port
    Given it is "red"s turn
    When they trade "wood" for "ore" with a "wood" port
    Then it should look exactly like "red trades [2 wood] to port wood for [1 ore]"

  Scenario: basic trade between player and brick port
    Given it is "red"s turn
    When they trade "brick" for "ore" with a "brick" port
    Then it should look exactly like "red trades [2 brick] to port brick for [1 ore]"

  Scenario: basic trade between player and wheat port
    Given it is "red"s turn
    When they trade "wheat" for "ore" with a "wheat" port
    Then it should look exactly like "red trades [2 wheat] to port wheat for [1 ore]"

  Scenario: basic trade between player and sheep port
    Given it is "red"s turn
    When they trade "sheep" for "ore" with a "sheep" port
    Then it should look exactly like "red trades [2 sheep] to port sheep for [1 ore]"

  Scenario: basic trade between player and ore port
    Given it is "red"s turn
    When they trade "ore" for "wood" with a "ore" port
    Then it should look exactly like "red trades [2 ore] to port ore for [1 wood]"

  Scenario: trade between two players
    Given it is "red"s turn
    When they trade "1" "wood" and "1" "brick" to player "red" for "2" "ore"
    Then it should look exactly like "red trades [1 wood, 1 brick] to player red for [2 ore]
