class RobotListenerExecution:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.tests = {}
        self._current_test_keywords = []
        self._current_test = None

    def start_suite(self, name, attributes):
        pass

    def start_test(self, name, attributes):
        self._current_test_keywords = []
        self._current_test = name
        self.tests[self._current_test] = {"keywords": [], "status": "running"}

    def start_keyword(self, name, attributes):
        self._current_test_keywords.append(attributes.get("kwname", name.split(".")[-1]))
        self.tests[self._current_test]["keywords"] = self._current_test_keywords.copy()

    def end_keyword(self, name, attributes):
        pass

    def log_message(self, message):
        self._current_test_keywords.append('log')
        self.tests[self._current_test]["keywords"] = self._current_test_keywords.copy()

    def end_test(self, name, attributes):
        self.tests[name] = {"keywords": self._current_test_keywords, "status": attributes.get("status", "pass")}

    def end_suite(self, name, attributes):
        pass

    def close(self):
        pass
