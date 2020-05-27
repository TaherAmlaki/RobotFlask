from robot import run
import secrets
from MyRobotRunners.RobotListenerExecution import RobotListenerExecution


class ExecuteRobotTests:
    def __init__(self):
        self.listener = None
        self.log_file = None

    def execute(self, suites: list, tests: list = None, options: dict = None):
        if options is None:
            options = {}
        if options.get("log"):
            options['outputdir'] = "../RobotReports"
        else:
            options['output'] = None
            options['report'] = None
        if options.get("listener") is None:
            self.listener = RobotListenerExecution()
            options['listener'] = self.listener
        if tests is not None:
            options['test'] = tests
        return run(*suites, **options)


# runner = ExecuteRobotTests()
# suites = ['../../Tests/GetStarWarsFilms.robot', '../../Tests/GetStarWarsPlanets.robot']
# tests = ['Get Film 1']
# # options = {"dryrun": "yes"}
# runner.execute(suites, tests)
# links = runner.listener.links
# print(len(links))
# for i in range(10):
#     print(links[i])
