class RobotOverviewListener:
    ROBOT_LISTENER_API_VERSION = 2
    SUITE_NAME = "SuiteName"
    SUITE_TESTS = "Tests"
    TEST_NAME = "TestName"
    TEST_STEPS = "TestSteps"

    def __init__(self):
        self.suites = []
        self._current_suite = {}
        self._current_test = {}

    def start_suite(self, name, attributes):
        self._current_suite[self.SUITE_NAME] = name
        self._current_suite[self.SUITE_TESTS] = []

    def start_test(self, name, attributes):
        self._current_test[self.TEST_NAME] = name
        self._current_test[self.TEST_STEPS] = []

    def start_keyword(self, name, attributes):
        self._current_test[self.TEST_STEPS].append(attributes.get("kwname", name))

    def end_test(self, name, attributes):
        self._current_suite[self.SUITE_TESTS].append(self._current_test.copy())
        self._current_test = {}

    def end_suite(self, name, attributes):
        self.suites.append(self._current_suite.copy())
        self._current_suite = {}
