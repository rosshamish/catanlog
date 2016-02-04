from behave import *
import hexgrid
import catanlog


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
