catanlog
--------

This project introduces a machine-parsable, human-readable file format for describing a game of Catan.

Each `.catan` file contains all publicly known information in the game. Therefore, each `.catan` file contains
sufficient information to 'replay' a game (from a spectator's point of view). This allows statistics and analysis to
be done after the fact, at any time.

This package is intended to support broadcast tooling (e.g. [catan-spectator](https://github.com/rosshamish/catan-spectator)), AI development (e.g. [goodcatan](https://github.com/rosshamish/goodcatan)), and other pursuits which benefit from well-defined game logs.

Until a formal specification is written, this implementation serves as the specification.
The spec will likely be formalized once stable, after v1.0.0

Supports Python 3. Might work in Python 2.

> Author: Ross Anderson ([rosshamish](https://github.com/rosshamish))

### Installation

```
pip install catanlog
```

### File Format


At a high level, files look like this:

```
version      |
timestamp    | Header
players      |
board layout |
...CATAN!    -
gameplay     | Body
```

The format is not yet v1.0, and could change at any time until then. The version is listed in version.py. Todos before
v1.0.0:
- test suite which enforces the syntax
- decide logged/not-logged for a) dev card types and b) *which* card was stolen in a robber move

Locations are integer coordinates of tiles, nodes and edges, as defined and computed by
module [`hexgrid`](https://github.com/rosshamish/hexgrid). Use it!

Coordinates are written to the log as (tile, direction) tuples for human readability. They look like this:

```
1         # the tile in the northwest corner
(1 NW)    # a node on the northwest corner of the board (settlement, city)
(1 NW)    # the edge on the northwest corner of the board (road)
```

### Usage

Each method of `catanlog.CatanLog` writes a single line to the log file (except `log_game_start`).
There is one method for each loggable action.

Many methods have parameter types from module [`catan`](https://github.com/rosshamish/catan-py) as parameters.
It isn't always obvious which type a parameter expects. That's a todo.

- Import it, create a logger

```
import catanlog

log = catanlog.CatanLog(use_stdout=True)
```

- Header / game start

```
log.log_game_start(players, terrain, numbers, ports)

catanlog v0.5.8                                          # version
timestamp: 2015-12-30 03:21:56.572418                    # timestamp
players: 4                                               # players
name: yurick, color: green, seat: 1                      #
name: josh, color: blue, seat: 2                         #
name: zach, color: orange, seat: 3                       #
name: ross, color: red, seat: 4                          #
terrain: desert brick sheep brick ... wheat wood         #
numbers: None 4 6 9 8 10 5 8 10 5 ... 9 12 11 6 4 2      # board layout
ports: wood(8 SE) brick(9 E) ... ore(2 W)  3:1(10 NE)    #
...CATAN!                                                # end header
```

- Rolling. Players are named by their color. Two is the only special one.

```
log.log_roll

green rolls 4
blue rolls 10
orange rolls 2 ...DEUCES!
```

- Moving the robber on a 7.

```
log.log_player_moves_robber_and_steals

green moves robber to 1, steals from red
```

- Buying and building. Note that the dev card type is not logged. This might change.

```
log.log_player_buys_XYZ

green buys settlement, builds at (1 NW)
blue buys city, builds at (1 SE)
orange buys road, builds at (2 E)
red buys dev card
```

- Trading. Multiple port trades in a turn can (and should) be consolidated into large port transactions.

```
log.log_player_trades_with_(player|port)

green trades [1 wheat, 1 brick] to player red for [1 sheep]
blue trades [3 wheat] to port 3:1 for [1 sheep]
orange trades [6 wheat] to port wheat for [3 ore]
```

- Dev cards. Note that when a knight is played and the robber is moved, one line is logged.
This differs from when a 7 is rolled and the robber is moved, when two lines are logged. They should probably be the
same.

```
log.log_player_plays_dev_XYZ

green plays knight
green moves robber to 1, steals from red
blue plays road builder, builds at (1 SW) and (1 W)
orange plays year of plenty, takes wood and brick
red plays monopoly on ore
green plays victory point
```

- End of turn. The length of the turn is logged, rounded to the nearest second.

```
log.log_player_ends_turn

green ends turn after 15s
```

- End of game.

```
log.log_player_wins

green wins
```

### License

GPLv3
