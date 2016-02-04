Feature: logging of player rolls

  Scenario: a dice roll which is not 2
    Given it is "red"s turn
    When a "6" is rolled
    Then it should look exactly like "red rolls 6"

  Scenario: a dice roll of 2
    Given it is "blue"s turn
    When a "2" is rolled
    Then it should look exactly like "blue rolls 2 ...DEUCES!"
