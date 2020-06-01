from datetime import datetime
from multiprocessing import cpu_count, Pool, Manager
from MyRobotRunners.ExecuteTests import ExecuteRobotTests
from MyRobotRunners.RobotListenerExecution import RobotListenerExecution


class ExecutionManager:
    MAX_NUMBER_OF_WORKERS = cpu_count() - 1

    def __init__(self, tests, suites):
        self._tests = tests
        self._suites = suites
        self.test2steps = {}
        self._test2ids = {}
        self._robot_suites = []
        self._robot_tests = []
        self._parallel_data = []
        self.prepared_tests = []
        self.logs = []
        self._queue = None
        self._prepare_data()

    def start(self):
        manager = Manager()
        self._queue = manager.Queue()

        test_data = []
        if self._tests.get("parallel", False):
            max_workers = min(ExecutionManager.MAX_NUMBER_OF_WORKERS, len(self._parallel_data))
            for test in self._parallel_data:
                listener = RobotListenerExecution()
                options = {"listener": listener, 'log': None}
                if self._tests.get("log"):
                    now = datetime.now().strftime("%Y%m%d_%H%M%S")
                    self.logs.append(f"log__{test['logName']}__{now}.html")
                    options['log'] = self.logs[-1]
                test_data.append([test['SuitePath'], test['TestName'], options, self._queue])
        else:
            max_workers = 1
            options = {"listener": RobotListenerExecution(), 'log': None}
            if self._tests.get("log"):
                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.logs.append(f"log__{now}.html")
                options['log'] = self.logs[0]
            consecutive_data = [self._robot_suites, self._robot_tests, options, self._queue]
            test_data.append(consecutive_data)

        pool = Pool(max_workers)
        pool.map(ExecuteRobotTests().execute, test_data)
        pool.close()
        pool.join()

    @property
    def status(self):
        percentages = {}
        if self._queue is None:
            return percentages

        while not self._queue.empty():
            data = self._queue.get()
            if data:
                for test_suite_name, val in data.items():
                    keywords = [k.lower() for k in val['keywords']]
                    status = val['status']
                    test_full_keywords = self.test2steps[test_suite_name]
                    p = 100.0 * len([s for s in test_full_keywords if s in keywords]) / len(test_full_keywords)
                    percentages[self._test2ids[test_suite_name]] = [round(p), status]
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
