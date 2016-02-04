"""
module catanlog provides a reference implementation for the catanlog (.catan) file format.

See class CatanLog for documentation.
"""
import copy
import datetime
import os
import sys

__version__ = '0.9.3'


class CatanLog(object):
    """
    class CatanLog introduces a machine-parsable, human-readable log of all actions made in a game of Catan.

    Each log contains all publicly known information in the game.
    Each log is sufficient to 'replay' a game from a spectator's point of view.

    This logger is for raw game actions only. No derivable or inferrable information will be logged.
    - e.g. players discarding cards on a 7 is not logged, because it is derivable from previous
           rolls, purchases, etc.

    The files are explicitly versioned by the class variable version, and versioning follows semver.

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

    def _log(self, content):
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
        self._log('{0}\n'.format(content))

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

        :param players: iterable of catan.game.Player objects
        :param terrain: list of 19 catan.board.Terrain objects.
        :param numbers: list of 19 catan.board.HexNumber objects.
        :param ports: list of catan.board.Port objects.
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
        :param player: catan.game.Player
        :param roll: integer or string, the sum of the dice
        """
        self._logln('{0} rolls {1}{2}'.format(player.color, roll, ' ...DEUCES!' if int(roll) == 2 else ''))

    def log_player_moves_robber_and_steals(self, player, location, victim):
        """
        :param player: catan.game.Player
        :param location: string, see hexgrid.location()
        :param victim: catan.game.Player
        """
        self._logln('{0} moves robber to {1}, steals from {2}'.format(
            player.color,
            location,
            victim.color
        ))

    def log_player_buys_road(self, player, location):
        """
        :param player: catan.game.Player
        :param location: string, see hexgrid.location()
        """
        self._logln('{0} buys road, builds at {1}'.format(
            player.color,
            location
        ))

    def log_player_buys_settlement(self, player, location):
        """
        :param player: catan.game.Player
        :param location: string, see hexgrid.location()
        """
        self._logln('{0} buys settlement, builds at {1}'.format(
            player.color,
            location
        ))

    def log_player_buys_city(self, player, location):
        """
        :param player: catan.game.Player
        :param location: string, see hexgrid.location()
        """
        self._logln('{0} buys city, builds at {1}'.format(
            player.color,
            location
        ))

    def log_player_buys_dev_card(self, player):
        """
        :param player: catan.game.Player
        """
        self._logln('{0} buys dev card'.format(
            player.color
        ))

    def log_player_trades_with_port(self, player, to_port, port, to_player):
        """
        :param player: catan.game.Player
        :param to_port: list of tuples, [(int, game.board.Terrain), (int, game.board.Terrain)]
        :param port: catan.board.Port
        :param to_player: list of tuples, [(int, game.board.Terrain), (int, game.board.Terrain)]
        """
        self._log('{0} trades '.format(player.color))

        # to_port items
        self._log('[')
        for i, (num, res) in enumerate(to_port):
            if i > 0:
                self._log(', ')
            self._log('{0} {1}'.format(num, res.value))
        self._log(']')

        self._log(' to port {0} for '.format(port.type.value))

        # to_player items
        self._log('[')
        for i, (num, res) in enumerate(to_player):
            if i > 0:
                self._log(', ')
            self._log('{0} {1}'.format(num, res.value))
        self._log(']')

        self._log('\n')

    def log_player_trades_with_other_player(self, player, to_other, other, to_player):
        """
        :param player: catan.game.Player
        :param to_other: list of tuples, [(int, game.board.Terrain), (int, game.board.Terrain)]
        :param other: catan.board.Player
        :param to_player: list of tuples, [(int, game.board.Terrain), (int, game.board.Terrain)]
        """
        self._log('{0} trades '.format(player.color))

        # to_other items
        self._log('[')
        for i, (num, res) in enumerate(to_other):
            if i > 0:
                self._log(', ')
            self._log('{0} {1}'.format(num, res.value))
        self._log(']')

        self._log(' to player {0} for '.format(other.color))

        # to_player items
        self._log('[')
        for i, (num, res) in enumerate(to_player):
            if i > 0:
                self._log(', ')
            self._log('{0} {1}'.format(num, res.value))
        self._log(']')

        self._log('\n')

    def log_player_plays_knight(self, player, location, victim):
        """
        :param player: catan.game.Player
        :param location: string, see hexgrid.location()
        :param victim: catan.game.Player
        """
        self._logln('{0} plays knight'.format(player.color))
        self.log_player_moves_robber_and_steals(player, location, victim)

    def log_player_plays_road_builder(self, player, location1, location2):
        """
        :param player: catan.game.Player
        :param location1: string, see hexgrid.location()
        :param location2: string, see hexgrid.location()
        """
        self._logln('{0} plays road builder, builds at {1} and {2}'.format(
            player.color,
            location1,
            location2
        ))

    def log_player_plays_year_of_plenty(self, player, resource1, resource2):
        """
        :param player: catan.game.Player
        :param resource1: catan.board.Terrain
        :param resource2: catan.board.Terrain
        """
        self._logln('{0} plays year of plenty, takes {1} and {2}'.format(
            player.color,
            resource1.value,
            resource2.value
        ))

    def log_player_plays_monopoly(self, player, resource):
        """
        :param player: catan.game.Player
        :param resource: catan.board.Terrain
        """
        self._logln('{0} plays monopoly on {1}'.format(
            player.color,
            resource.value
        ))

    def log_player_plays_victory_point(self, player):
        """
        :param player: catan.game.Player
        """
        self._logln('{0} plays victory point'.format(player.color))

    def log_player_ends_turn(self, player):
        """
        :param player: catan.game.Player
        """
        seconds_delta = (datetime.datetime.now() - self._latest_timestamp).total_seconds()
        self._logln('{0} ends turn after {1}s'.format(player.color, round(seconds_delta)))
        self._latest_timestamp = datetime.datetime.now()

    def log_player_wins(self, player):
        """
        :param player: catan.game.Player
        """
        self._logln('{0} wins'.format(player.color))

    def _log_board_terrain(self, terrain):
        """
        Tiles are logged counterclockwise beginning from the top-left.
        See module hexgrid (https://github.com/rosshamish/hexgrid) for the tile layout.

        :param terrain: list of catan.board.Terrain objects
        """
        self._logln('terrain: {0}'.format(' '.join(t.value for t in terrain)))

    def _log_board_numbers(self, numbers):
        """
        Numbers are logged counterclockwise beginning from the top-left.
        See module hexgrid (https://github.com/rosshamish/hexgrid) for the tile layout.

        :param numbers: list of catan.board.HexNumber objects.
        """
        self._logln('numbers: {0}'.format(' '.join(str(n.value) for n in numbers)))

    def _log_board_ports(self, ports):
        """
        A board with no ports is allowed.

        In the logfile, ports must be sorted
        - ascending by tile identifier (primary)
        - alphabetical by edge direction (secondary)

        :param ports: list of catan.board.Port objects
        """
        ports = sorted(ports, key=lambda port: (port.tile_id, port.direction))
        self._logln('ports: {0}'.format(' '.join('{}({} {})'.format(p.type.value, p.tile_id, p.direction)
                                                for p in ports)))

    def _log_players(self, players):
        """
        :param players: list of catan.game.Player objects
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
