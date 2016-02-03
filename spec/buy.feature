Feature: logging of buying and building

  Scenario: buying and building a road
    Given it is "red"s turn
    When they buy a road and build it at "1" "NW"
    Then it should look exactly like "red buys road, builds at (1 NW)"

  Scenario: buying and building a settlement
    Given it is "blue"s turn
    When they buy a settlement and build it at "1" "NW"
    Then it should look exactly like "blue buys settlement, builds at (1 NW)"

  Scenario: buying and building a city
    Given it is "orange"s turn
    When they buy a city and build it at "1" "NW"
    Then it should look exactly like "orange buys city, builds at (1 NW)"

  Scenario: buying a development card
    Given it is "white"s turn
    When they buy a dev card
    Then it should look exactly like "white buys dev card"
