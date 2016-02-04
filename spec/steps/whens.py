from behave import *
import hexgrid
from catan.game import Player
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


@when('they play a knight, move the robber to "{location}" and steal from "{color}"')
def step_impl(context, location, color):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_plays_dev_knight,
                               context.cur_player,
                               location,
                               Player(1, 'name', color))


@when('they play a road builder, building at "{location1}" and "{location2}"')
def step_impl(context, location1, location2):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_plays_dev_road_builder,
                               context.cur_player,
                               location1,
                               location2)


@when('they play a year of plenty, taking "{resource1}" and "{resource2}"')
def step_impl(context, resource1, resource2):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_plays_dev_year_of_plenty,
                               context.cur_player,
                               resource1,
                               resource2)


@when('they play a monopoly on "{resource}"')
def step_impl(context, resource):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_plays_dev_monopoly,
                               context.cur_player,
                               resource)


@when('they play a victory point')
def step_impl(context):
    context.output = output_of(context.logger,
                               catanlog.CatanLog.log_player_plays_dev_victory_point,
                               context.cur_player)
