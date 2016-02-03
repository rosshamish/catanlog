from behave import *
import catanlog


def output_of(log, method, *args, **kwargs):
    method(log, *args, **kwargs)
    with open(log.logpath(), 'r') as fp:
        lines = [line.rstrip() for line in fp.readlines()]
    return lines


@when('the game starts')
def step_game_start(context):
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
def step_roll(context, roll):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_roll,
                               context.cur_player,
                               roll)
