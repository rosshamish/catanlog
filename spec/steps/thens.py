from behave import *
import re


@then('it will look exactly like "{text}"')
def step_look_exactly_like(context, text):
    print(context.output)
    assert len(context.output) == 1
    assert text == context.output[0]


@then('it will look exactly like')
def step_look_like(context):
    """Compares text as written to the log output"""
    expected_lines = context.text.split('\n')
    assert len(expected_lines) == len(context.output)
    for expected, actual in zip(expected_lines, context.output):
        print('--\n\texpected: {}\n\tactual: {}'.format(expected, actual))
        assert expected == actual


@then('it will look like "{regex}"')
def step_look_like_regex(context, regex):
    print(context.output)
    assert len(context.output) == 1
    assert re.fullmatch(regex, context.output[0])


@then('it will look like')
def step_look_like(context):
    """Compares text as regex to the log output"""
    expected_lines = context.text.split('\n')
    assert len(expected_lines) == len(context.output)
    for expected, actual in zip(expected_lines, context.output):
        print('--\n\texpected: {}\n\tactual: {}'.format(expected, actual))
        assert re.match(expected, actual)


@then('print output')
def step_print_output(context):
    print(context.output)
    assert False
