from behave import *
from catan import boardbuilder
from catan.game import Player


@given('we have the default players')
def step_impl(context):
    context.players = [Player(1, 'ross', 'red'),
                       Player(2, 'zach', 'orange'),
                       Player(3, 'josh', 'blue'),
                       Player(4, 'yuri', 'green')]


@given('we have the default board')
def step_impl(context):
    context.board = boardbuilder.build({
        'terrain': 'preset',
        'numbers': 'preset',
        'ports': 'preset'
    })


@given('it is the first player\'s turn')
def step_impl(context):
    context.cur_player = context.players[0]


@given('it is "{color}"s turn')
def step_impl(context, color):
    context.cur_player = Player(1, 'name', color)
