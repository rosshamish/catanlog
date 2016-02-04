Feature: logging of the game header

  Scenario: the start of a default game
    Given we have the default players
    And we have the default board
    When the game starts
    Then it should look like
    """
    catanlog v\d+\.\d+\.\d+
    timestamp: \d{4}-[01]\d-[0-3]\d [0-2]\d:[0-5]\d:[0-5]\d
    players: 4
    name: ross, color: red, seat: 1
    name: zach, color: orange, seat: 2
    name: josh, color: blue, seat: 3
    name: yuri, color: green, seat: 4
    terrain: wood wheat ore wheat sheep brick sheep wheat wood ore brick desert wheat sheep wood ore sheep wood brick
    numbers: 5 2 6 3 8 10 9 12 11 4 8 None 10 9 4 5 6 3 11
    ports: 3:1\(1 NW\) wood\(2 W\) brick\(4 W\) 3:1\(5 SW\) 3:1\(6 SE\) sheep\(8 SE\) 3:1\(9 E\) ore\(10 NE\) wheat\(12 NE\)
    ...CATAN!
    """
