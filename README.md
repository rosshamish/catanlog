catanlog
--------

Human-readable, machine-parsable file format for describing a game of Catan.

Also, a reference Python implementation: `catanlog.Writer`.

The format is described by a human-readable behavioural specification in `spec`.
The spec is not yet v1.0.0, so there might be some breaking changes until then.

Each `.catan` file contains all publicly known information in the game. Therefore, each `.catan` file contains
sufficient information to 'replay' a game (from a spectator's point of view). This allows statistics and analysis to
be done after the fact, which is very useful.

This package is intended to support broadcast tooling (e.g. [catan-spectator](https://github.com/rosshamish/catan-spectator)), AI development (e.g. [goodcatan](https://github.com/rosshamish/goodcatan)), and other pursuits which would benefit from well-defined game logs.

Supports Python 3.

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

The specification is defined by .feature files in `spec/`. The `.feature` files are human-readable. They are executed
using [behave](https://github.com/behave/behave).

`$ behave spec/`

The format is not yet v1.0, and could change at any time until then. The version is listed in version.py. Todos before
v1.0.0:
- decide logged/not-logged for a) dev card types and b) *which* card was stolen in a robber move

### Usage

There is one method in class CatanLog for each loggable action.

Some methods expect parameters of types defined in module [`catan`](https://github.com/rosshamish/catan-py). Methods are
documented individually, check the docstring.

Methods which take a `location` expect location strings as computed by method `location()` in
module [`hexgrid`](https://github.com/rosshamish/hexgrid). Use it! Locations look like this:

```
1         # the tile in the northwest corner
(1 NW)    # a node on the northwest corner of the board (settlement, city)
(1 NW)    # the edge on the northwest corner of the board (road)
```

The tile numbers start from 1 in the northwest corner, and increase counterclockwise, spiralling inwards. See the
documentation of [`hexgrid`](https://github.com/rosshamish/hexgrid) for more info.

Examples:

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
log.log_player_roll(player, roll)

green rolls 4
blue rolls 10
orange rolls 2 ...DEUCES!
```

- Moving the robber on a 7.

```
log.log_player_moves_robber_and_steals(player, location, victim)

green moves robber to 1, steals from red
```

- Buying and building. Note that the dev card type is not logged. This might change.

```
log.log_player_buys_road(player, location)
log.log_player_buys_settlement(player, location)
log.log_player_buys_city(player, city)
log.log_player_buys_dev_card(player)

green buys settlement, builds at (1 NW)
blue buys city, builds at (1 SE)
orange buys road, builds at (2 E)
red buys dev card
```

- Trading. Multiple port trades in a turn can (and should) be consolidated into large port transactions.

```
log.log_player_trades_with_port(player, to_port, port, to_player)
log.log_player_trades_with_other_player(player, to_other, other, to_player)

green trades [1 wheat, 1 brick] to player red for [1 sheep]
blue trades [3 wheat] to port 3:1 for [1 sheep]
orange trades [6 wheat] to port wheat for [3 ore]
```

- Dev cards.

```
log.log_player_plays_knight(player, location, victim)
log.log_player_plays_road_builder(player, location1, location2)
log.log_player_plays_year_of_plenty(player, resource1, resource2)
log.log_player_plays_monopoly(player, resource)
log.log_player_plays_victory_point(player)

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
