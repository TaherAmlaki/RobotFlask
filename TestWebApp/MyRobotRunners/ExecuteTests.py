from robot import run
from MyRobotRunners.RobotListenerExecution import RobotListenerExecution


class ExecuteRobotTests:
    def __init__(self):
        self.listener = None
        self.log_file = None
        self._queue = None

    def execute(self, data: list):
        suites, tests, options, queue = data
        self._queue = queue
        if options is None:
            options = {}
        if options.get("log"):
            options['outputdir'] = "../RobotReports"
        else:
            options['output'] = None
            options['report'] = None
        if options.get("listener") is None:
            self.listener = RobotListenerExecution()
        else:
            self.listener = options.get('listener')
            self.listener.queue = queue
        options['listener'] = self.listener
        if tests is not None:
            options['test'] = tests
        return run(*suites, **options)

