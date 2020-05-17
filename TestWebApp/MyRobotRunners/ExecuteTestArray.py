from threading import Thread
from MyRobotRunners.ExecuteTests import ExecuteRobotTests
from MyRobotRunners.RobotListenerExecution import RobotListenerExecution


class ExecutionManager:
    def __init__(self, tests, suites):
        self._tests = tests
        self._suites = suites
        self._threads = []
        self._listener = RobotListenerExecution()
        self.test2steps = {}
        self._test2ids = {}

    def start(self):
        self._map_tests()
        suites = list(set([t['SuiteShortPath'] for t in self._tests['Tests']]))
        tests = [t['TestName'] for t in self._tests['Tests']]
        execution = ExecuteRobotTests()
        execution.execute(suites, tests, {"listener": self._listener})

    def get_status(self):
        percentages = {}
        for test_name, keywords_status in self._listener.tests.items():
            keywords = [k.lower() for k in keywords_status['keywords']]
            test_full_keywords = self.test2steps[test_name]
            p = 100.0 * len([s for s in test_full_keywords if s in keywords]) / len(test_full_keywords)
            percentages[self._test2ids[test_name]] = [round(p), keywords_status['status']]
        return percentages

    def _map_tests(self):
        self.test2steps = {}
        for suite in self._suites:
            for test in suite.get("Tests", []):
                self.test2steps[test['TestName']] = [str(step['step']).lower() for step in test['TestSteps']]
                self._test2ids[test['TestName']] = test['TestID']
