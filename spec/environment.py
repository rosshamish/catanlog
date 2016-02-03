import shutil


def after_scenario(context, scenario):
    # erase the log file after each scenario
    with open(context.logger.logpath(), 'w'):
        pass


def after_all(context):
    # erase the log directory after each test run
    shutil.rmtree('spec/log')
