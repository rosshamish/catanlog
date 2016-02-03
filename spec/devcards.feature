Feature: logging of development card plays

  Scenario: play a knight card
    Given it is "green"s turn
    When they play a knight, move the robber to "1" and steal from "red"
    Then it should look exactly like
    """
    green plays knight
    green moves the robber to 1, steals from red
    """

  Scenario: play a knight card, but they can't steal from anyone
    Given it is "green"s turn
    When they play a knight, move the robber to "1" and steal from "nobody"
    Then it should look exactly like
    """
    green plays knight
    green moves the robber to 1, steals from nobody
    """

  Scenario: play a road builder card
    Given it is "orange"s turn
    When they play a road builder, building at "1" "NW" and "1 W"
    Then it should look exactly like "orange plays road builder, builds at (1 NW) and (1 W)

  Scenario: play a year of plenty card
    Given it is "white"s turn
    When they play a year of plenty, taking "wood" and "brick"
    Then it should look exactly like "white plays year of plenty, takes wood and brick

  Scenario: play a year of plenty card, taking two of the same
    Given it is "red"s turn
    When they play a year of plenty, taking "ore" and "ore"
    Then it should look exactly like "red plays year of plenty, takes ore and ore"

  Scenario: play a monopoly card
    Given it is "blue"s turn
    When they play a monopoly on "ore"
    Then it should look exactly like "blue plays monopoly on ore"

  Scenario: play a victory point card
    Given it is "red"s turn
    When the play a victory point
    Then it should look exactly like "red plays victory point"

