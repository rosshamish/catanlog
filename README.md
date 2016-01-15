catanlog
--------

reference implementation for the catanlog (.catan) file format

This project introduces a machine-parsable, human-readable file format for describing a game of Catan.

Until a formal specification is written, this implementation serves as the specification. The spec will likely be formalized once stable, after v1.0.0

Supports Python 3. Might work in Python 2.

> Author: Ross Anderson ([rosshamish](https://github.com/rosshamish))

### Installation

```
pip install catanlog
```

### File Format

Each `.catan` file contains all publicly known information in the game.
Therefore, each `.catan` file contains sufficient information to 'replay' a game (from a spectator's point of view).

The header begins with a version, and ends with `...CATAN!`. The game begins after that.

Tiles are numbered 1 through 19 starting from the most northwest tile and spiralling countercockwise inward.
See module hexgrid (`hexgrid.py`) for details.

The format is not yet v1.0, and could change at any time until then.

Example

```
catanlog v0.5.5
timestamp: 2015-12-30 03:21:56.572418
players: 4
name: yurick, color: green, seat: 1
name: josh, color: blue, seat: 2
name: zach, color: orange, seat: 3
name: ross, color: red, seat: 4
terrain: desert brick sheep brick ore brick wheat wood wood wheat wood sheep ore wood sheep sheep wheat ore wheat
numbers: None 4 6 9 8 10 5 8 10 5 3 11 3 9 12 11 6 4 2
ports: 3:1(1 NW) ore(2 W) 3:1(4 W) sheep(5 SW) 3:1(6 SE) wood(8 SE) brick(9 E) 3:1(10 NE) wheat(12 NE)
...CATAN!
green buys settlement, builds at (17 NW)
green buys road, builds at (17 NW)
green ends turn
blue buys settlement, builds at (8 NW)
blue buys road, builds at (8 NW)
blue ends turn
orange buys settlement, builds at (3 SE)
orange buys road, builds at (3 SE)
orange ends turn
red buys settlement, builds at (5 NE)
red buys road, builds at (5 E)
red ends turn
red buys settlement, builds at (13 S)
red buys road, builds at (13 SE)
red ends turn
orange buys settlement, builds at (10 NW)
orange buys road, builds at (11 SW)
orange ends turn
blue buys settlement, builds at (9 NW)
blue buys road, builds at (9 NW)
blue ends turn
green buys settlement, builds at (2 SW)
green buys road, builds at (2 W)
green ends turn
green rolls 4
green buys road, builds at (2 NW)
green ends turn
blue rolls 2 ...DEUCES!
blue plays dev card: road builder, builds at (9 W) and (10 E)
blue buys settlement, builds at (10 NE)
blue trades [1 wheat, 1 brick] to player green for [1 sheep]
```

See `catanlog.CatanLog` for all available actions, along with their format.

### License

GPLv3
