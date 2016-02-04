from behave import *
import re


@then('it should look exactly like "{text}"')
def step_impl(context, text):
    print(context.output)
    assert len(context.output) == 1
    assert text == context.output[0]


@then('it should look exactly like')
def step_impl(context):
    """Compares text as written to the log output"""
    expected_lines = context.text.split('\n')
    assert len(expected_lines) == len(context.output)
    for expected, actual in zip(expected_lines, context.output):
        print('--\n\texpected: {}\n\tactual: {}'.format(expected, actual))
        assert expected == actual


@then('it should look like "{regex}"')
def step_impl(context, regex):
    print(context.output)
    assert len(context.output) == 1
    assert re.fullmatch(regex, context.output[0])


@then('it should look like')
def step_impl(context):
    """Compares text as regex to the log output"""
    expected_lines = context.text.split('\n')
    assert len(expected_lines) == len(context.output)
    for expected, actual in zip(expected_lines, context.output):
        print('--\n\texpected: {}\n\tactual: {}'.format(expected, actual))
        assert re.match(expected, actual)


@then('print output')
def step_impl(context):
    print(context.output)
    assert False
