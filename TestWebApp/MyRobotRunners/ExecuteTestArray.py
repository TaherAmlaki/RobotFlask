from datetime import datetime
import concurrent.futures
import multiprocessing
from MyRobotRunners.ExecuteTests import ExecuteRobotTests
from MyRobotRunners.RobotListenerExecution import RobotListenerExecution


class ExecutionManager:
    MAX_NUMBER_OF_WORKERS = 4

    def __init__(self, tests, suites):
        self._tests = tests
        self._suites = suites
        self._threads = []
        self._listeners = []
        self.test2steps = {}
        self._test2ids = {}
        self._robot_suites = []
        self._robot_tests = []
        self._parallel_data = []
        self.prepared_tests = []
        self.logs = []
        self._prepare_data()

    def start(self):
        if self._tests.get("parallel", False):
            max_workers = min(ExecutionManager.MAX_NUMBER_OF_WORKERS, len(self._parallel_data))
            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
                processes = []
                for test in self._parallel_data:
                    self._listeners.append(RobotListenerExecution())
                    options = {"listener": self._listeners[-1], 'log': None}
                    if self._tests.get("log"):
                        now = datetime.now().strftime("%Y%m%d_%H%M%S")
                        self.logs.append(f"log__{test['logName']}__{now}.html")
                        options['log'] = self.logs[-1]
                    robot_executor = ExecuteRobotTests()
                    p = executor.submit(robot_executor.execute, test['SuitePath'], test['TestName'], options)
                    processes.append(p)
                # TODO: handle exceptions by iterating through results

        else:
            self._listeners.append(RobotListenerExecution())
            options = {"listener": self._listeners[0], 'log': None}
            if self._tests.get("log"):
                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.logs.append(f"log__{now}.html")
                options['log'] = self.logs[0]
            robot_executor = ExecuteRobotTests()
            robot_executor.execute(self._robot_suites, self._robot_tests, options)

    @property
    def status(self):
        percentages = {}
        for listener in self._listeners:
            print("listener data is: ", listener.tests)
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
            suite_name = test['data']['SuiteName']
            suite_relative_path = test['data']['SuiteShortPath']
            suites.append(suite_relative_path)

            if test['type'] == 'suite':
                tests += [t['TestName'] for t in test['data']['Tests']]
                for t in test['data']['Tests']:
                    test_name = t['TestName']
                    test_relative_path = suite_relative_path + "/" + test_name
                    self.prepared_tests.append({"TestName": test_name,
                                                'TestID': t['TestID'],
                                                "RelativePath": test_relative_path})
                    log_name = f'{suite_name.replace(" ", "_")}_{test_name.replace(" ", "_")}'
                    self._parallel_data.append({"TestName": [test_name],
                                                "SuitePath": [suite_relative_path],
                                                "logName": log_name})
            else:
                test_name = test['data']['TestName']
                tests.append(test_name)
                test_relative_path = test['data']['SuiteShortPath'] + "/" + test_name
                self.prepared_tests.append({"TestName": test_name,
                                            'TestID': test['data']['TestID'],
                                            "RelativePath": test_relative_path})
                log_name = f'{suite_name.replace(" ", "_")}_{test_name.replace(" ", "_")}'
                self._parallel_data.append({"TestName": [test_name],
                                            "SuitePath": [suite_relative_path],
                                            "logName": log_name})
        self._robot_suites = list(set(suites))
        self._robot_tests = list(set(tests))

    def _map_tests(self):
        self.test2steps = {}
        for suite in self._suites:
            for test in suite.get("Tests", []):
                self.test2steps[(suite['SuiteName'], test['TestName'])] = [str(step['step']).lower() for step in test['TestSteps']]
                self._test2ids[(suite['SuiteName'], test['TestName'])] = test['TestID']


