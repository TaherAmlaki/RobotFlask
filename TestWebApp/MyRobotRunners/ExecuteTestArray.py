from datetime import datetime
from MyRobotRunners.ExecuteTests import ExecuteRobotTests
from MyRobotRunners.RobotListenerExecution import RobotListenerExecution


class ExecutionManager:

    def __init__(self, tests, suites):
        self._tests = tests
        self._suites = suites
        self._threads = []
        self._listeners = []
        self.test2steps = {}
        self._test2ids = {}
        self._robot_suites = []
        self._robot_tests = []
        self.prepared_tests = []
        self.logs = []
        self._prepare_data()

    def start(self):
        self._listeners.append(RobotListenerExecution())
        options = {"listener": self._listeners[0], 'log': None}
        if self._tests.get("log"):
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.logs.append(f"log_{now}.html")
            options['log'] = self.logs[0]
        execution = ExecuteRobotTests()
        execution.execute(self._robot_suites, self._robot_tests, options)

    @property
    def status(self):
        percentages = {}
        for listener in self._listeners:
            for test_suite_name, keywords_status in listener.tests.items():
                keywords = [k.lower() for k in keywords_status['keywords']]
                test_full_keywords = self.test2steps[test_suite_name]
                p = 100.0 * len([s for s in test_full_keywords if s in keywords]) / len(test_full_keywords)
                percentages[self._test2ids[test_suite_name]] = [round(p), keywords_status['status']]
        return percentages

    def _prepare_data(self):
        self._map_tests()
        suites = []
        tests = []
        for test in self._tests['Tests']:
            if test['type'] == 'suite':
                tests += [t['TestName'] for t in test['data']['Tests']]
                suite_relative_path = test['data']['SuiteShortPath']
                suites.append(suite_relative_path)
                for t in test['data']['Tests']:
                    test_relative_path = suite_relative_path + "/" + t['TestName']
                    self.prepared_tests.append({"TestName": t['TestName'],
                                                'TestID': t['TestID'],
                                                "RelativePath": test_relative_path})
            else:
                tests.append(test['data']['TestName'])
                suites.append(test['data']['SuiteShortPath'])
                test_relative_path = test['data']['SuiteShortPath'] + "/" + test['data']['TestName']
                self.prepared_tests.append({"TestName": test['data']['TestName'],
                                            'TestID': test['data']['TestID'],
                                            "RelativePath": test_relative_path})
        self._robot_suites = list(set(suites))
        self._robot_tests = list(set(tests))

    def _map_tests(self):
        self.test2steps = {}
        for suite in self._suites:
            for test in suite.get("Tests", []):
                self.test2steps[(suite['SuiteName'], test['TestName'])] = [str(step['step']).lower() for step in test['TestSteps']]
                self._test2ids[(suite['SuiteName'], test['TestName'])] = test['TestID']


