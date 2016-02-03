import shutil
import catanlog


def before_scenario(context, scenario):
    # create a catanlog
    context.logger = catanlog.CatanLog(auto_flush=True, log_dir='spec/log', use_stdout=False)

def after_scenario(context, scenario):
    # erase the log file after each scenario
    with open(context.logger.logpath(), 'w'):
        pass


def after_all(context):
    # erase the log directory after each test run
    shutil.rmtree('spec/log')
