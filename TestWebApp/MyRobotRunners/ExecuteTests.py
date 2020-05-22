from robot import run
from datetime import datetime
from MyRobotRunners.RobotListenerExecution import RobotListenerExecution


class ExecuteRobotTests:
    def __init__(self):
        self.listener = None
        self.execution_threads = []

    def execute(self, suites: list, tests: list = None, options: dict = None):
        if options is None:
            options = {}
        # if options.get("log") is None:
        #     now = datetime.now().strftime("%Y%m%d_%H%M%S")
        #     options['log'] = f"RobotLog_{now}.html"
        if options.get("listener") is None:
            self.listener = RobotListenerExecution()
            options['listener'] = self.listener
        if tests is not None:
            options['test'] = tests
        return run(*suites, **options)


# runner = ExecuteRobotTests()
# suites = [r"G:\Mijn Documenten\pega-testfiles\outreach\Test suites\reminderProcessTestCases.robot"]
# tests = ["NP Nationality Flow - No EDB"]
# options = {"dryrun": "yes"}
# runner.execute(suites, tests, options)
# links = runner.listener.links
# print(len(links))
# for i in range(10):
#     print(links[i])
