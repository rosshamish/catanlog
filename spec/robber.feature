Feature: logging of moving the robber and stealing from players

  Scenario: moving the robber, stealing from a player
    Given it is "red"s turn
    When they move the robber to "1" and steal from "blue"
    Then it should look exactly like "red moves robber to 1, steals from blue"

  Scenario: moving the robber, stealing from nobody
    Given it is "red"s turn
    When they move the robber to "1" and steal from "nobody"
    Then it should look exactly like "red moves robber to 1, steals from nobody"
