from behave import *
import catanlog
import catan.game
import catan.board


def output_of(log, method, *args, **kwargs):
    method(log, *args, **kwargs)
    with open(log.logpath(), 'r') as fp:
        lines = [line.rstrip() for line in fp.readlines()]
    return lines


@when('the game starts')
def step_impl(context):
    terrain = list()
    numbers = list()
    for tile in context.board.tiles:
        terrain.append(tile.terrain)
        numbers.append(tile.number)
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_game_start,
                               context.players,
                               terrain,
                               numbers,
                               context.board.ports)


@when('a "{roll}" is rolled')
def step_impl(context, roll):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_roll,
                               context.cur_player,
                               roll)


@when('they win the game')
def step_impl(context):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_wins,
                               context.cur_player)


@when('they end their turn')
def step_impl(context):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_ends_turn,
                               context.cur_player)


@when('they move the robber to "{location}" and steal from "{color}"')
def step_impl(context, location, color):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_moves_robber_and_steals,
                               context.cur_player,
                               location,
                               catan.game.Player(1, 'name', color))


@when('they buy a "{piece}" and build it at "{location}"')
def step_impl(context, piece, location):
    if piece == 'road':
        method = catanlog.CatanLog.log_player_buys_road
    elif piece == 'settlement':
        method = catanlog.CatanLog.log_player_buys_settlement
    elif piece == 'city':
        method = catanlog.CatanLog.log_player_buys_city
    else:
        raise ValueError('piece must be on of: road, settlement, city')

    context.output = output_of(context.logger,
                               method,
                               context.cur_player,
                               location)


@when('they buy a dev card')
def step_impl(context):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_buys_dev_card,
                               context.cur_player)


@when('they play a knight, move the robber to "{location}" and steal from "{color}"')
def step_impl(context, location, color):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_plays_knight,
                               context.cur_player,
                               location,
                               catan.game.Player(1, 'name', color))


@when('they play a road builder, building at "{location1}" and "{location2}"')
def step_impl(context, location1, location2):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_plays_road_builder,
                               context.cur_player,
                               location1,
                               location2)


@when('they play a year of plenty, taking "{resource1}" and "{resource2}"')
def step_impl(context, resource1, resource2):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_plays_year_of_plenty,
                               context.cur_player,
                               catan.board.Terrain(resource1),
                               catan.board.Terrain(resource2))


@when('they play a monopoly on "{resource}"')
def step_impl(context, resource):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_plays_monopoly,
                               context.cur_player,
                               catan.board.Terrain(resource))


@when('they play a victory point')
def step_impl(context):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_plays_victory_point,
                               context.cur_player)


@when('they trade "{give}" for "{get}" with a "{port}" port')
def step_impl(context, give, get, port):
    valid_resources = {'wood', 'brick', 'wheat', 'sheep', 'ore'}
    if port == '4:1':
        num_give = 4
    elif port == '3:1':
        num_give = 3
    elif port in valid_resources:
        num_give = 2
    else:
        raise ValueError('invalid port: {}'.format(port))

    if give not in valid_resources:
        raise ValueError('invalid resource to give: {}'.format(give))

    if get not in valid_resources:
        raise ValueError('invalid resource to get: {}'.format(get))

    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_trades_with_port,
                               context.cur_player,
                               [(num_give, catan.board.Terrain(give))],
                               catan.board.Port(1, 'N', catan.board.PortType(port)),
                               [(1, catan.board.Terrain(get))])


@when('they compound trade "{num_give1}" "{give1}" and "{num_give2}" "{give2}" for "{get}" with a "{port}" port')
def step_impl(context, num_give1, give1, num_give2, give2, get, port):
    valid_resources = {'wood', 'brick', 'wheat', 'sheep', 'ore'}
    valid_ports = {'4:1', '3:1'}
    for res in valid_resources:
        valid_ports.add(res)

    if give1 not in valid_resources:
        raise ValueError('invalid resource to give: {}'.format(give1))
    if give2 not in valid_resources:
        raise ValueError('invalid resource to give: {}'.format(give2))
    if get not in valid_resources:
        raise ValueError('invalid resource to get: {}'.format(get))

    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_trades_with_port,
                               context.cur_player,
                               [(num_give1, catan.board.Terrain(give1)), (num_give2, catan.board.Terrain(give2))],
                               catan.board.Port(1, 'N', catan.board.PortType(port)),
                               [(2, catan.board.Terrain(get))])


@when('they trade "{num_give1}" "{give1}" and "{num_give2}" "{give2}" to player "{color}" for "{num_get}" "{get}"')
def step_impl(context, num_give1, give1, num_give2, give2, color, num_get, get):
    valid_resources = {'wood', 'brick', 'wheat', 'sheep', 'ore'}

    if give1 not in valid_resources:
        raise ValueError('invalid resource to give: {}'.format(give1))
    if give2 not in valid_resources:
        raise ValueError('invalid resource to give: {}'.format(give2))
    if get not in valid_resources:
        raise ValueError('invalid resource to get: {}'.format(get))

    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_trades_with_other_player,
                               context.cur_player,
                               [(num_give1, catan.board.Terrain(give1)), (num_give2, catan.board.Terrain(give2))],
                               catan.game.Player(1, 'name', color),
                               [(num_get, catan.board.Terrain(get))])
