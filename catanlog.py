"""
module catanlog provides a reference implementation for the catanlog (.catan) file format.

See class CatanLog for documentation.
"""
import copy
import datetime
import os
import sys

__version__ = '0.9.1'


class CatanLog(object):
    """
    class CatanLog introduces a machine-parsable, human-readable log of all actions made in a game of Catan.

    Each log contains all publicly known information in the game.
    Each log is sufficient to 'replay' a game from a spectator's point of view.

    This logger is for raw game actions only. No derivable or inferrable information will be logged.
    - e.g. players discarding cards on a 7 is not logged, because it is derivable from previous
           rolls, purchases, etc.

    The files are explicitly versioned by the class variable version, and versioning follows semver.

    See individual methods' documentation for syntax and intent. Syntax variables are as follows:
    - $color is the color of a player, eg 'red', 'blue', 'green', 'orange'
    - $name is the name of a player, eg 'josh', 'yurick', 'zach', 'ross'
    - $seat is the seat number of a player, eg 1, 2, 3, 4
    - $number is an integer number, eg 7, 2, 3, 11, 12
    - $location is a tile identifier and an optional direction, eg 1, 2, (1 NW), (2 W)
    - $port is the name of a port, eg 4:1, 3:1, wood, brick, wheat
    - $resource is the name of a terrain, resource, or card, eg wood, brick, wheat
    - $num is an integer value on the range [0,inf)

    Use #dump to get the log as a string.
    Use #flush to write the log to a file.

    TODO maybe log private information as well (which dev card picked up, which card stolen)
    """
    def __init__(self, auto_flush=True, log_dir='log', use_stdout=False):
        """
        Create a CatanLog object using the given options. The defaults are fine.

        :param auto_flush: flush the log to file after every log() call, bool
        :param log_dir: directory to write the log to, str
        :param use_stdout: if True, flush() will write to stdout instead of to file
        """
        self._buffer = str()

        self._chars_flushed = 0
        self._auto_flush = auto_flush
        self._log_dir = log_dir
        self._use_stdout = use_stdout

        self._game_start_timestamp = datetime.datetime.now()
        self._latest_timestamp = copy.deepcopy(self._game_start_timestamp)
        self._players = list()

    def _dolog(self, content):
        """
        Write a string to the log
        """
        self._buffer += content
        if self._auto_flush:
            self.flush()

    def _logln(self, content):
        """
        Write a string to the log, appending a newline
        """
        self._dolog('{0}\n'.format(content))

    def eraseln(self):
        """
        Erase the latest line from the log
        """
        self._buffer = '\n'.join(self._buffer.split('\n')[:-2])

    def reset(self):
        """
        Erase the log and reset the timestamp
        """
        self._buffer = ''
        self._chars_flushed = 0
        self._game_start_timestamp = datetime.datetime.now()

    def dump(self):
        """
        Dump the entire log to a string, and return it
        """
        return self._buffer

    def _latest(self):
        """
        Get all characters written to _log since the last flush()
        """
        return self._buffer[self._chars_flushed:]

    def logpath(self):
        """
        Return the logfile path and filename as a string.

        The file with name self.logpath() is written to on flush().

        The filename contains the log's timestamp and the names of players in the game.
        The logpath changes when reset() or _set_players() are called, as they change the
        timestamp and the players, respectively.
        """
        name = '{}-{}.catan'.format(self.timestamp_str(),
                                    '-'.join([p.name for p in self._players]))
        path = os.path.join(self._log_dir, name)
        if not os.path.exists(self._log_dir):
            os.mkdir(self._log_dir)
        return path

    def timestamp_str(self):
        return self._game_start_timestamp.strftime('%Y-%m-%d %H:%M:%S')

    def flush(self):
        """
        Append the latest updates to file, or optionally to stdout instead. See the constructor
        for logging options.
        """
        latest = self._latest()
        self._chars_flushed += len(latest)
        if self._use_stdout:
            file = sys.stdout
        else:
            file = open(self.logpath(), 'a')

        print(latest, file=file, flush=True, end='')

        if not self._use_stdout:
            file.close()

    def log_game_start(self, players, terrain, numbers, ports):
        """
        Begin a game.

        Erase the log, set the timestamp, set the players, and write the log header.

        The robber is assumed to start on the desert (or off-board).

        :param players: set of 3 or (ideally) 4 Players
        :param terrain: list of 19 Terrains. Proper rules: 3 each of (brick, ore), 4 each of all others
        :param numbers: list of 19 HexNumbers. Proper rules: 1 each of (2, 12), 2 each of all others.
        :param ports: list of Ports
        """
        self.reset()
        self._set_players(players)
        self._logln('{} v{}'.format(__name__, __version__))
        self._logln('timestamp: {0}'.format(self.timestamp_str()))
        self._log_players(players)
        self._log_board_terrain(terrain)
        self._log_board_numbers(numbers)
        self._log_board_ports(ports)
        self._logln('...CATAN!')

    def log_player_roll(self, player, roll):
        """
        syntax: $color rolls $number

        alternate syntax: if roll == 2, syntax: $color rolls $number ...DEUCES!
        """
        self._logln('{0} rolls {1}{2}'.format(player.color, roll, ' ...DEUCES!' if int(roll) == 2 else ''))

    def log_player_moves_robber_and_steals(self, player, tile_id, victim):
        """
        syntax: $color moves robber to $location, steals from $color
        """
        self._logln('{0} moves robber to {1}, steals from {2}'.format(
            player.color,
            tile_id,
            victim.color
        ))

    def log_player_buys_settlement(self, player, location):
        """
        syntax: $color buys settlement, builds at $location
        """
        self._logln('{0} buys settlement, builds at {1}'.format(
            player.color,
            location
        ))

    def log_player_buys_city(self, player, location):
        """
        syntax: $color buys city, builds at $location
        """
        self._logln('{0} buys city, builds at {1}'.format(
            player.color,
            location
        ))

    def log_player_buys_dev_card(self, player):
        """
        syntax: $color buys dev card
        """
        self._logln('{0} buys dev card'.format(
            player.color
        ))

    def log_player_buys_road(self, player, location):
        """
        syntax: $color buys road, builds at $location
        """
        self._logln('{0} buys road, builds at {1}'.format(
            player.color,
            location
        ))

    def log_player_trades_with_port(self, player, to_port, port, to_player):
        """
        syntax: $color trades $number $resource[, $number resource]* to port $port for $number $resource[, $number resource]*

        :param to_port: list of tuples: [(2, 'wood'), (2, 'brick')]
        :param to_player: list of tuples: [(1, 'ore'), (1, 'sheep')]
        """
        self._dolog('{0} trades '.format(player))

        # to_other items
        self._dolog('[')
        for i, (num, res) in enumerate(to_port):
            if i > 0:
                self._dolog(',')
            self._dolog('{0} {1}'.format(num, res))
        self._dolog(']')

        self._dolog(' to port {0} for '.format(port))

        # to_player items
        self._dolog('[')
        for i, (num, res) in enumerate(to_player):
            if i > 0:
                self._dolog(',')
            self._dolog('{0} {1}'.format(num, res))
        self._dolog(']')

        self._dolog('\n')

    def log_player_trades_with_other(self, player, to_other, other, to_player):
        """
        syntax: $color trades [$number $resources, $number resources] to player $color for [$number $resources, $number resources]

        :param to_other: list of tuples: [(2, 'wood'), (2, 'brick')]
        :param to_player: list of tuples: [(1, 'ore'), (1, 'sheep')]
        """
        self._dolog('{0} trades '.format(player))

        # to_other items
        self._dolog('[')
        for i, (num, res) in enumerate(to_other):
            if i > 0:
                self._dolog(', ')
            self._dolog('{0} {1}'.format(num, res))
        self._dolog(']')

        self._dolog(' to player {0} for '.format(other))

        # to_player items
        self._dolog('[')
        for i, (num, res) in enumerate(to_player):
            if i > 0:
                self._dolog(', ')
            self._dolog('{0} {1}'.format(num, res))
        self._dolog(']')

        self._dolog('\n')

    def log_player_plays_dev_knight(self, player, tile_id, victim):
        """
        syntax (two lines):
        $color plays knight
        $color moves robber to $location, steals from $color
        """
        self._logln('{0} plays knight'.format(player))
        self.log_player_moves_robber_and_steals(player, tile_id, victim)

    def log_player_plays_dev_monopoly(self, player, resource):
        """
        syntax: $color plays monopoly on $resource
        """
        self._logln('{0} plays monopoly on {1}'.format(
            player.color,
            resource
        ))

    def log_player_plays_dev_year_of_plenty(self, player, resource1, resource2):
        """
        syntax: $color plays year of plenty, takes $resource and $resource
        """
        self._logln('{0} plays year of plenty, takes {1} and {2}'.format(
            player.color,
            resource1,
            resource2
        ))

    def log_player_plays_dev_victory_point(self, player):
        """
        syntax: $color plays victory point
        """
        self._logln('{0} plays victory point'.format(player.color))

    def log_player_plays_dev_road_builder(self, player, location1, location2):
        """
        syntax: $color plays road builder, builds at $location and $location
        """
        self._logln('{0} plays road builder, builds at {1} and {2}'.format(
            player.color,
            location1,
            location2
        ))

    def log_player_ends_turn(self, player):
        """
        syntax: $color ends turn after $(num)s
        """
        seconds_delta = (datetime.datetime.now() - self._latest_timestamp).total_seconds()
        self._logln('{0} ends turn after {1}s'.format(player.color, round(seconds_delta)))
        self._latest_timestamp = datetime.datetime.now()

    def log_player_wins(self, player):
        """
        syntax: $color wins
        """
        self._logln('{0} wins'.format(player.color))

    def _log_board_terrain(self, terrain):
        """
        syntax: terrain: ($resource ){19}

        Tiles are logged counterclockwise beginning from the top-left.
        See module hexgrid (hexgrid.py) for the tile layout.

        There are 19 tiles in the base catan board.

        :param terrain: list of 19 resources in models.Terrain, eg ['wood', 'brick', 'wood', 'desert', 'ore', ...]
        """
        self._logln('terrain: {0}'.format(' '.join(t.value for t in terrain)))

    def _log_board_numbers(self, numbers):
        """
        syntax: numbers: ($number ){19}

        Numbers are logged counterclockwise beginning from the top-left.
        See module hexgrid (hexgrid.py) for the tile layout.

        There are 19 tiles in the base catan board.

        None designates a tile where there is no number. Usually, this is
        the desert.

        :param numbers: list of 19 HexNumbers
        """
        self._logln('numbers: {0}'.format(' '.join(str(n.value) for n in numbers)))

    def _log_board_ports(self, ports):
        """
        syntax: ports: ($port$location)*

        A board with no ports is allowed.

        In the logfile, ports must be sorted
        - ascending by tile identifier (primary)
        - alphabetical by edge direction (secondary)

        :param ports: list of Ports
        """
        ports = sorted(ports, key=lambda port: (port.tile_id, port.direction))
        self._logln('ports: {0}'.format(' '.join('{}({} {})'.format(p.type.value, p.tile_id, p.direction)
                                                for p in ports)))

    def _log_players(self, players):
        """
        syntax:
        players: $number
        (name: $name, color: $color, seat: $number
        )+
        """
        self._logln('players: {0}'.format(len(players)))
        for p in self._players:
            self._logln('name: {0}, color: {1}, seat: {2}'.format(p.name, p.color, p.seat))

    def _set_players(self, _players):
        """
        Players will always be set in seat order (1,2,3,4)
        """
        self._players = list()
        _players = list(_players)
        _players.sort(key=lambda p: p.seat)
        for p in _players:
            self._players.append(p)


class NoopCatanLog(object):
    """
    class NoopCatanLog implements no-op versions of all methods defined by CatanLog.

    It can be used in place of a CatanLog instance if the caller does not want any
    logging to occur.
    """
    def __getattr__(self, name):
        def method(*args):
            return None
        return method
